import httpx
import os

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://localhost:8000")

async def save_question_to_main_backend(question_data: dict):
    url = f"{MAIN_BACKEND_URL}/add-question"
    headers = {
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=question_data, headers=headers)
        response.raise_for_status()
        return response.json()
