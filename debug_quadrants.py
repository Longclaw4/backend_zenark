import motor.asyncio
import asyncio
import os
from dotenv import load_dotenv
import statistics

async def check():
    load_dotenv('Heatblast/.env')
    mongo_uri = os.getenv('MONGO_URI')
    client = motor.asyncio.AsyncIOMotorClient(mongo_uri)
    db = client.get_default_database()
    
    # 1. Get students
    students = await db.users.find({"role": "student"}).to_list(1000)
    student_emails = [s.get("email") for s in students if s.get("email")]
    student_ids = [str(s["_id"]) for s in students]
    
    # 2. Get marks
    all_marks = await db.marks.find({}).to_list(5000)
    student_marks = {}
    for m in all_marks:
        sid = str(m.get("student_id") or m.get("userId") or m.get("user_id") or m.get("email") or "")
        val = m.get("marks") or m.get("score") or m.get("percentage")
        if sid and val is not None:
            try:
                if sid not in student_marks: student_marks[sid] = []
                student_marks[sid].append(float(val))
            except: pass
            
    # 3. Get wellness (Mock for now or check reports)
    reports = await db.reports.find({}).to_list(1000)
    wellness_map = {}
    for r in reports:
        uid = str(r.get("userId") or r.get("user_id") or r.get("email") or "")
        score = r.get("score") or r.get("mental_wellness") or 7.5
        try:
            score = float(score)
            if score <= 10: score *= 10
            wellness_map[uid] = score
        except: pass

    # 4. Categorize
    stars, plateaued, climbers, critical = 0, 0, 0, 0
    for s in students:
        uid = str(s["_id"])
        email = s.get("email")
        marks_list = student_marks.get(uid) or student_marks.get(email) or []
        acad_avg = statistics.mean(marks_list) if marks_list else 75
        wellness = wellness_map.get(uid) or wellness_map.get(email) or 80
        
        if acad_avg >= 80 and wellness >= 70: stars += 1
        elif acad_avg >= 80 and wellness < 70: plateaued += 1
        elif acad_avg < 80 and wellness >= 70: climbers += 1
        else: critical += 1
        
    print(f"Total Students: {len(students)}")
    print(f"Stars: {stars}")
    print(f"Plateaued: {plateaued}")
    print(f"Climbers: {climbers}")
    print(f"Critical: {critical}")

if __name__ == "__main__":
    asyncio.run(check())
