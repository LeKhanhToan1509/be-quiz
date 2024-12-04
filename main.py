from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import json

app = FastAPI()

# CORS Middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Allow frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class Question(BaseModel):
    question: str
    options: list
    correctOption: int
    points: int

# Load questions from file
def load_questions_from_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

questions_data = load_questions_from_file("quiz_data.json")

@app.get("/random-questions")
def get_random_questions(n: int = 50):
    if not questions_data.get("questions"):
        return {"error": "No questions found in the data file."}
    
    random_questions = random.sample(questions_data["questions"], min(n, len(questions_data["questions"])))
    return {"questions": random_questions}
