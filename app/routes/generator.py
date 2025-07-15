







from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # même fake URL ici

from fastapi import APIRouter, HTTPException, Query, Depends
from app.models.quiz import QuestionCreate
from app.services.openai_service import generate_question
from app.db import db
from app.auth import admin_required  # pour sécuriser l'accès
import asyncio

router = APIRouter()

@router.post("/generate-and-save", response_model=dict)
async def generate_and_save(theme: str = Query(...), user=Depends(admin_required)):
    try:
        # Générer une question à l'aide d'OpenAI
        loop = asyncio.get_running_loop()
        raw_question = await loop.run_in_executor(None, generate_question, theme)
        question_data = QuestionCreate(**raw_question)

        # Vérifier que le thème existe
        theme_doc = await db.themes.find_one({"name": question_data.theme})
        if not theme_doc:
            raise HTTPException(status_code=404, detail="Thème non trouvé.")

        # Vérifier que la bonne réponse est dans les options
        if question_data.correct_answer not in question_data.options:
            raise HTTPException(status_code=400, detail="La réponse correcte doit être dans les options.")

        # Ajouter la question à la base de données
        await db.questions.insert_one(question_data.dict())

        return {
            "message": "Question générée et ajoutée avec succès !",
            "question": question_data.dict()
        }

    except Exception as e:
        raise HTTPException(500, detail=str(e))
