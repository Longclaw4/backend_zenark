from pymongo import MongoClient
import os
from dotenv import load_dotenv

def list_collections():
    load_dotenv(dotenv_path="Heatblast/.env")
    mongo_uri = os.getenv("MONGO_DB_OFFICIAL")
    db_name = os.getenv("MONGO_DB_NAME_OFFICIAL")
    
    print(f"Connecting to: {db_name}")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    
    collections = db.list_collection_names()
    print("Collections:")
    for c in collections:
        print(f" - {c}")
        # Print count
        count = db[c].count_documents({})
        print(f"   (count: {count})")

if __name__ == "__main__":
    list_collections()
