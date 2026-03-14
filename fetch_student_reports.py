from pymongo import MongoClient
import os
from bson import json_util
import json

def get_reports():
    uri = "mongodb+srv://zenark:rzZfbYJQAxdMGGKI@cluster0.30zvh8x.mongodb.net/zenark?retryWrites=true&w=majority"
    db_name = "zenark"
    
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[db_name]
    
    # Try common roll numbers from db_dump
    emails = ["440930@zenark.in", "440198@zenark.in"]
    
    try:
        for email in emails:
            print(f"\nSearching reports for: {email}")
            reports = list(db["reports"].find({"userId": email}).limit(2))
            if not reports:
                # Try user_id instead of userId
                reports = list(db["reports"].find({"user_id": email}).limit(2))
                
            if reports:
                for r in reports:
                    print(f"Report found! Keys: {list(r.keys())}")
                    # Print interesting parts
                    print(f"Wellness: {r.get('wellness_score') or r.get('mental_wellness')}")
                    print(f"Strengths: {r.get('strengths')}")
                    print(f"Weaknesses: {r.get('weaknesses')}")
            else:
                print("No reports found for this email")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_reports()
