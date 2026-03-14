import motor.asyncio
import asyncio
import os
from dotenv import load_dotenv

async def check():
    load_dotenv('Heatblast/.env')
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("MONGO_URI not found")
        return
        
    client = motor.asyncio.AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    
    print("Checking collections...")
    collections = await db.list_collection_names()
    print(f"Collections: {collections}")
    
    # Check users collection for students and productivity data
    if 'users' in collections:
        print("\nChecking 'users' collection for students...")
        student = await db.users.find_one({"role": "student"})
        if student:
            print(f"Found a student: {student.get('name')} ({student.get('email')})")
            print(f"Keys in user object: {list(student.keys())}")
            if 'productivity' in student:
                print(f"Productivity data for student: {student['productivity']}")
            else:
                print("No 'productivity' field found in student object.")
        else:
            print("No students found in 'users' collection.")

if __name__ == "__main__":
    asyncio.run(check())
