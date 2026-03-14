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
    
    print("Checking 'reports' collection...")
    reports = await db.reports.find().sort("timestamp", -1).limit(10).to_list(10)
    if not reports:
        print("No reports found")
    for r in reports:
        score = r.get('score')
        student = r.get('student_id') or r.get('email')
        ts = r.get('timestamp')
        print(f"Student: {student}, Score: {score}, Timestamp: {ts}")

if __name__ == "__main__":
    asyncio.run(check())
