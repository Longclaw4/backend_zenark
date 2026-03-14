import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

async def debug_reports():
    load_dotenv()
    mongo_uri = os.getenv("MONGO_DB_OFFICIAL")
    db_name = os.getenv("MONGO_DB_NAME_OFFICIAL")
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    
    # Emails seen in the screenshot console
    emails = ["340973@zenark.in", "440930@zenark.in", "440314@zenark.in"]
    
    print(f"Checking reports in {db_name} for identifiers...")
    
    for email in emails:
        print(f"\n--- Identifying reports for {email} ---")
        # Check by all possible fields
        query = {
            "$or": [
                {"userId": email},
                {"user_id": email},
                {"student_id": email},
                {"email": email}
            ]
        }
        count = await db["reports"].count_documents(query)
        print(f"Found {count} reports matching email {email}")
        
        if count > 0:
            sample = await db["reports"].find_one(query)
            print(f"Sample report keys: {list(sample.keys())}")
            print(f"Identifiers in sample: userId={sample.get('userId')}, user_id={sample.get('user_id')}, student_id={sample.get('student_id')}, email={sample.get('email')}")
        else:
            # Let's see what identifiers DO exist in the reports collection
            print("No match for email. Checking sample IDs from the collection...")
            sample_ids = await db["reports"].find({}, {"userId": 1, "user_id": 1}).limit(5).to_list(length=5)
            print(f"Sample identifiers in collection: {sample_ids}")

if __name__ == "__main__":
    asyncio.run(debug_reports())
