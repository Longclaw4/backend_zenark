from pymongo import MongoClient
import os
from dotenv import load_dotenv

def get_test_student():
    load_dotenv(dotenv_path="Heatblast/.env")
    mongo_uri = os.getenv("MONGO_DB_OFFICIAL")
    db_name = os.getenv("MONGO_DB_NAME_OFFICIAL")
    
    client = MongoClient(mongo_uri)
    db = client[db_name]
    
    # Try to find a student in class MAD-1
    student = db["users"].find_one({"class": {"$regex": "MAD-1", "$options": "i"}, "role": "student"})
    if student:
        print(f"ID: {student['_id']}")
        print(f"Email: {student.get('email')}")
        print(f"Name: {student.get('name')}")
    else:
        print("No student found in MAD-1")

if __name__ == "__main__":
    get_test_student()
