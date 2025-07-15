import os
import openai
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

import random

def generate_question(theme: str):
    random_seed = random.randint(1, 1_000_000)
    prompt = f"""
Seed: {random_seed}

Generate a multiple-choice quiz question on the theme '{theme}' in this JSON format:

{{
  "question": "...",
  "options": ["...", "...", "...", "..."],
  "correct_answer": "...",
  "theme": "{theme}"
}}

Rules:
- Return only a single JSON object
- Only one correct answer
- Options should be shuffled
- Keep difficulty: medium
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,  # légèrement plus élevé
    )
    return json.loads(response.choices[0].message.content.strip())