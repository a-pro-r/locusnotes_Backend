import aiohttp
import asyncio
import uuid
from datetime import datetime


async def test_create_note():
    url = 'http://localhost:8000/api/v1/notes'

    test_note = {
        "user_id": "7dd28284-477d-48b2-b65e-d2e4b62d2a0d",  # Fixed user ID
        "title": "Test Note @ walmart",
        "content": "Test Content",
        "tags": ["test"],
        "location_name": "Test Location",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "address": "123 Test St"
    }

    try:
        async with aiohttp.ClientSession() as session:
            print(f"\nTrying to create note...")
            async with session.post(url, json=test_note) as response:
                status = response.status
                result = await response.json()
                print(f"Status Code: {status}")
                print(f"Response: {result}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    print("Starting API tests...")
    asyncio.run(test_create_note())