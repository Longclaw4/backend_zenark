import httpx
import asyncio
import json

async def check_prajwal():
    async with httpx.AsyncClient() as client:
        # Prajwal's email from the screenshot
        email = "141866@zenark.in"
        url = f"http://localhost:8000/api/dashboard/student-report/{email}"
        
        print(f"Fetching report for: {email}")
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"Status: {data.get('status')}")
                history = data.get('history', [])
                print(f"Found {len(history)} history entries.")
                for i, r in enumerate(history):
                    print(f"Entry {i+1}: score={r.get('score')}, timestamp={r.get('timestamp')}")
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_prajwal())
