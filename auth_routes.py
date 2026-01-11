"""
Authentication Routes for Zenark API
Implements: signup, signin, signout, changepassword, changename
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import bcrypt
import jwt
import datetime
from bson import ObjectId
import os
import logging

logger = logging.getLogger("zenark.auth")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-this-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# ============================================================
# PYDANTIC MODELS
# ============================================================

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    school: str
    class_name: str = ""  # Using class_name instead of class (reserved keyword)
    roles: list[str] = ["student"]

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

class ChangeNameRequest(BaseModel):
    email: EmailStr
    new_name: str
    token: str

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt_token(user_id: str, email: str) -> str:
    """Create a JWT token for a user"""
    payload = {
        "id": user_id,
        "email": email,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt_token(token: str) -> dict:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ============================================================
# DATABASE HELPER (will be injected from main app)
# ============================================================

users_collection = None

def set_users_collection(collection):
    """Set the users collection from the main app"""
    global users_collection
    return collection

# ============================================================
# AUTHENTICATION ENDPOINTS
# ============================================================

@router.post("/signup")
async def signup(request: SignupRequest):
    """
    User registration endpoint
    
    Creates a new user account with hashed password.
    Returns success message on successful registration.
    """
    try:
        if users_collection is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": request.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Duplicate username or role doesn't exist")
        
        # Validate roles
        valid_roles = ["student", "teacher", "admin", "moderator"]
        for role in request.roles:
            if role not in valid_roles:
                raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
        
        # Hash the password
        hashed_password = hash_password(request.password)
        
        # Create user document
        user_doc = {
            "name": request.name,
            "email": request.email,
            "password": hashed_password,
            "school": request.school,
            "class": request.class_name,
            "roles": request.roles,
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }
        
        # Insert into database
        result = await users_collection.insert_one(user_doc)
        
        logger.info(f"✅ New user registered: {request.email}")
        
        return JSONResponse(
            status_code=200,
            content={"message": "Registered successfully", "user_id": str(result.inserted_id)}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Signup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signin")
async def signin(request: SigninRequest):
    """
    User login endpoint
    
    Authenticates user and returns JWT token.
    Returns 401 for invalid credentials.
    """
    try:
        if users_collection is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # Find user by email
        user = await users_collection.find_one({"email": request.email})
        
        if not user:
            logger.warning(f"⚠️  Login attempt for non-existent user: {request.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(request.password, user["password"]):
            logger.warning(f"⚠️  Invalid password for user: {request.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create JWT token
        token = create_jwt_token(str(user["_id"]), user["email"])
        
        logger.info(f"✅ User logged in: {request.email}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": str(user["_id"]),
                    "email": user["email"],
                    "name": user["name"],
                    "roles": user.get("roles", []),
                    "school": user.get("school", ""),
                    "class": user.get("class", "")
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Signin error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signout")
async def signout():
    """
    User logout endpoint
    
    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token. This endpoint is here for API completeness.
    """
    return JSONResponse(
        status_code=200,
        content={"message": "Logged out successfully"}
    )


@router.post("/changepassword")
async def change_password(request: ChangePasswordRequest):
    """
    Change user password endpoint
    
    Requires old password verification before changing to new password.
    """
    try:
        if users_collection is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # Find user
        user = await users_collection.find_one({"email": request.email})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify old password
        if not verify_password(request.old_password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid old password")
        
        # Hash new password
        new_hashed_password = hash_password(request.new_password)
        
        # Update password
        await users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "password": new_hashed_password,
                    "updated_at": datetime.datetime.utcnow()
                }
            }
        )
        
        logger.info(f"✅ Password changed for user: {request.email}")
        
        return JSONResponse(
            status_code=200,
            content={"message": "Password changed successfully"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Change password error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/changename")
async def change_name(request: ChangeNameRequest):
    """
    Change user name endpoint
    
    Requires valid JWT token.
    """
    try:
        if users_collection is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        # Verify token
        payload = decode_jwt_token(request.token)
        
        # Find user
        user = await users_collection.find_one({"email": request.email})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify token belongs to this user
        if payload["id"] != str(user["_id"]):
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        # Update name
        await users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "name": request.new_name,
                    "updated_at": datetime.datetime.utcnow()
                }
            }
        )
        
        logger.info(f"✅ Name changed for user: {request.email}")
        
        return JSONResponse(
            status_code=200,
            content={"message": "Name changed successfully", "new_name": request.new_name}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Change name error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
