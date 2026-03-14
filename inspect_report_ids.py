import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

async def inspect_identifiers():
    # Load from the correct absolute path
    dot_env_path = r"c:\Users\vaibh\OneDrive\Desktop\Mental_Study_Chat-main\Heatblast\.env"
    load_dotenv(dot_env_path)
    
    mongo_uri = os.getenv("MONGO_DB_OFFICIAL")
    db_name = os.getenv("MONGO_DB_NAME_OFFICIAL")
    
    if not mongo_uri:
        print("ERROR: MONGO_DB_OFFICIAL not found in .env")
        return

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    
    print(f"Inspecting 'reports' collection in {db_name}...")
    
    # Get 20 reports to understand the identifier pattern
    cursor = db["reports"].find({}, {"userId": 1, "user_id": 1, "email": 1, "student_id": 1}).sort("_id", -1).limit(20)
    reports = await cursor.to_list(length=20)
    
    if not reports:
        print("No reports found in the collection.")
        return

    print(f"Found {len(reports)} reports. Identifier samples:")
    for i, r in enumerate(reports):
        print(f"{i+1}. userId: {r.get('userId')} | user_id: {r.get('user_id')} | email: {r.get('email')} | student_id: {r.get('student_id')}")

if __name__ == "__main__":
    asyncio.run(inspect_identifiers())
