import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

async def check_db_insights():
    load_dotenv()
    mongo_uri = os.getenv("MONGO_DB_OFFICIAL")
    db_name = os.getenv("MONGO_DB_NAME_OFFICIAL")
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    
    print(f"Checking collection: reports in {db_name}")
    # Find a few reports that have strengths or weaknesses
    cursor = db["reports"].find({"$or": [{"strengths": {"$exists": True, "$ne": []}}, {"weaknesses": {"$exists": True, "$ne": []}}]}).limit(3)
    reports = await cursor.to_list(length=3)
    
    if not reports:
        print("No reports with qualitative insights found in the 'reports' collection.")
        return

    for doc in reports:
        print(f"\nReport for User ID: {doc.get('userId')}")
        print(f"Strengths: {doc.get('strengths')}")
        print(f"Weaknesses: {doc.get('weaknesses')}")

if __name__ == "__main__":
    asyncio.run(check_db_insights())
