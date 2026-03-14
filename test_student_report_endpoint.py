import httpx
import asyncio
import json

async def test_student_report():
    async with httpx.AsyncClient() as client:
        # Test with a known email from db_dump
        student_email = "440930@zenark.in"
        url = f"http://localhost:8000/api/dashboard/student-report/{student_email}"
        
        try:
            print(f"Testing endpoint: {url}")
            response = await client.get(url)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Success!")
                print(f"Student ID: {data.get('student_id')}")
                print(f"History count: {len(data.get('history', []))}")
                if data.get('history'):
                    print("Sample History Entry:")
                    print(json.dumps(data['history'][0], indent=2))
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Failed to reach backend: {e}")

if __name__ == "__main__":
    asyncio.run(test_student_report())
