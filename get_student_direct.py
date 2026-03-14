from pymongo import MongoClient
import os

def get_test_student():
    uri = "mongodb+srv://zenark:rzZfbYJQAxdMGGKI@cluster0.30zvh8x.mongodb.net/zenark?retryWrites=true&w=majority"
    db_name = "zenark"
    
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[db_name]
    
    try:
        # Get one student
        student = db["users"].find_one({"role": "student"})
        if student:
            print(f"ID: {student['_id']}")
            print(f"Email: {student.get('email')}")
            print(f"Name: {student.get('name')}")
        else:
            print("No student found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_test_student()
