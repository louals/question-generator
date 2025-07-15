from fastapi import APIRouter, HTTPException, Query
from app.models.quiz import QuestionCreate
from app.services.openai_service import generate_question
from app.services.question_saver import save_question_to_main_backend
import asyncio

router = APIRouter()

@router.post("/generate-and-save", response_model=dict)
async def generate_and_save(theme: str = Query(...)):
    try:
        loop = asyncio.get_running_loop()
        # Call sync OpenAI function in thread executor
        question = await loop.run_in_executor(None, generate_question, theme)

        # Save generated question to main backend
        result = await save_question_to_main_backend(question)

        return {
            "message": "Question generated and saved successfully!",
            "backend_response": result,
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))
