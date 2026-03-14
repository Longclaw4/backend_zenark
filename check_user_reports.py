import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId

async def check_user():
    dot_env_path = r"c:\Users\vaibh\OneDrive\Desktop\Mental_Study_Chat-main\Heatblast\.env"
    load_dotenv(dot_env_path)
    
    mongo_uri = os.getenv("MONGO_DB_OFFICIAL")
    db_name = os.getenv("MONGO_DB_NAME_OFFICIAL")
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    
    email = "340973@zenark.in"
    print(f"Searching for user: {email}")
    
    user = await db["users"].find_one({"email": email})
    if user:
        print(f"✅ Found user: {user.get('name')}")
        print(f"User ID (_id): {user.get('_id')} (type: {type(user.get('_id'))})")
        
        # Now check if there are reports for this ID
        uid = user.get('_id')
        query = {"$or": [
            {"userId": uid},
            {"userId": str(uid)},
            {"user_id": uid},
            {"user_id": str(uid)},
            {"email": email}
        ]}
        report_count = await db["reports"].count_documents(query)
        print(f"Reports found for user {uid}: {report_count}")
        
        if report_count > 0:
            sample = await db["reports"].find_one(query)
            print(f"Sample report userId: {sample.get('userId')} (type: {type(sample.get('userId'))})")
    else:
        print(f"❌ User {email} not found in users collection.")

if __name__ == "__main__":
    asyncio.run(check_user())
