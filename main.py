from fastapi import FastAPI
from app.routes import generator

app = FastAPI()
app.include_router(generator.router, prefix="/question-gen")