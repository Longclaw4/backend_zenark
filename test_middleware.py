from fastapi import FastAPI, Request, Depends
from fastapi.testclient import TestClient
from auth_middleware import JWTAuthenticationMiddleware
import jwt
import datetime

# Minimal app for testing
app = FastAPI()
app.add_middleware(JWTAuthenticationMiddleware)

@app.get("/test-protected")
async def protected_route(request: Request):
    user = getattr(request.state, "user", None)
    if user:
        return {"authenticated": True, "user": user}
    return {"authenticated": False, "message": "No user found"}

# Configuration (Matches auth_routes.py)
JWT_SECRET = "your-secret-key-change-this-in-production"
JWT_ALGORITHM = "HS256"

def create_test_token(user_id="test_user_123", email="test@example.com"):
    payload = {
        "id": user_id,
        "email": email,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def run_test():
    client = TestClient(app)
    
    # 1. Test without token
    print("Testing without token...")
    response = client.get("/test-protected")
    print(f"Result: {response.json()}")
    
    # 2. Test with valid token
    print("\nTesting with valid token...")
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/test-protected", headers=headers)
    print(f"Result: {response.json()}")
    
    # 3. Test with invalid token
    print("\nTesting with invalid token...")
    headers = {"Authorization": "Bearer invalid-token-here"}
    response = client.get("/test-protected", headers=headers)
    print(f"Result: {response.json()}")

if __name__ == "__main__":
    try:
        run_test()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please make sure 'fastapi', 'httpx', and 'pyjwt' are installed.")
