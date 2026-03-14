from pymongo import MongoClient
import os
from dotenv import load_dotenv

def check_marks_schema():
    load_dotenv(dotenv_path="Heatblast/.env")
    mongo_uri = os.getenv("MONGO_DB_OFFICIAL")
    db_name = os.getenv("MONGO_DB_NAME_OFFICIAL")
    
    print(f"Connecting to: {db_name}")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    
    print("Checking 'marks' collection...")
    cursor = db["marks"].find({"$or": [{"strengths": {"$exists": True}}, {"weaknesses": {"$exists": True}}]}).limit(3)
    marks = list(cursor)
    
    if not marks:
        print("No documents with 'strengths' or 'weaknesses' found in 'marks' collection.")
        # Let's check a general sample
        sample = db["marks"].find_one()
        print(f"General sample keys: {list(sample.keys()) if sample else 'None'}")
    else:
        for m in marks:
            print(f"Mark doc ID: {m['_id']}")
            print(f"Strengths: {m.get('strengths')}")
            print(f"Weaknesses: {m.get('weaknesses')}")

if __name__ == "__main__":
    check_marks_schema()
