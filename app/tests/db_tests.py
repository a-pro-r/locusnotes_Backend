import aiohttp
import asyncio
import uuid
from datetime import datetime

from numpy.compat import asunicode


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

async def get_note_by_id():
    note_id = "ad83213a-8554-4ca3-93f1-086686e672d9"
    url = f'http://localhost:8000/api/v1/notes/{note_id}'
    try:
        async with aiohttp.ClientSession() as session:
            print(f"\n Retrieving note...")
            async with session.get(url) as response:
                status = response.status
                result = await response.json()
                print(f"Status Code: {status}")
                print(f"Response: {result}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

async def get_note_by_userid():
    user_id = "7dd28284-477d-48b2-b65e-d2e4b62d2a0d"
    url = f'http://localhost:8000/api/v1/notes/user/{user_id}'
    try:
        async with aiohttp.ClientSession() as session:
            print(f"\n Retrieving note...")
            async with session.get(url) as response:
                status = response.status
                result = await response.json()
                print(f"Status Code: {status}")
                print(f"Response: {result}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def test_update_note():
    note_id = "ad83213a-8554-4ca3-93f1-086686e672d9"
    url = f'http://localhost:8000/api/v1/notes/{note_id}'

    updated_note = {
        "user_id": "7dd28284-477d-48b2-b65e-d2e4b62d2a0d", # Test User ID
        "title": "Updated Test Note @ walmart",
        "content": "Updated Test Content",
        "tags": ["test", "updated"],
        "location_name": "Updated Test Location",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "address": "123 Updated Test St"
    }

    try:
        async with aiohttp.ClientSession() as session:
            print(f"\nTrying to update note...")
            async with session.put(url, json=updated_note) as response:
                status = response.status
                result = await response.json()
                print(f"Status Code: {status}")
                print(f"Response: {result}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def test_delete_note():
    note_id = "19c16912-3e44-46bf-8720-34e500474e5b"
    user_id = "7dd28284-477d-48b2-b65e-d2e4b62d2a0d"
    url = f'http://localhost:8000/api/v1/notes/{note_id}'


    params = {'user_id': user_id}  # As query param

    try:
        async with aiohttp.ClientSession() as session:
            print(f"\nTrying to delete note...")
            async with session.delete(url, params=params) as response:
                status = response.status
                print(f"Status Code: {status}")
                if status == 204:
                    print("Note successfully deleted")
                else:
                    result = await response.json()
                    print(f"Response: {result}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

async def test_register_user():
    url = 'http://localhost:8000/api/v1/users/register'
    test_user = {
        "email": "test_script@example.com"
    }

    try:
        async with aiohttp.ClientSession() as session:
            print(f"\nTrying to register user...")
            async with session.post(url, json=test_user) as response:
                status = response.status
                result = await response.json()
                print(f"Status Code: {status}")
                print(f"Response: {result}")

                if status == 201:
                    user_id = result["id"]
                    print(f"User registered successfully with ID: {user_id}")
                    return user_id
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    print("Starting API tests...")
    # asyncio.run(test_create_note())
    # asyncio.run(get_note_by_id())
    # asyncio.run(get_note_by_userid())
    # asyncio.run(test_update_note())
    # asyncio.run(test_delete_note())
    asyncio.run(test_register_user())