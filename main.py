import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(
    title="EduGenie AI",
    description="A Gemini-powered learning assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None


class LearningRequest(BaseModel):
    question: Optional[str] = ""
    topic: Optional[str] = ""
    text: Optional[str] = ""
    level: Optional[str] = "beginner"
    num_questions: Optional[int] = 5


def ask_gemini(prompt: str) -> str:
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured."
        )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text or "No response generated."
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini request failed: {str(exc)}"
        )


@app.get("/")
def home():
    return {
        "message": "Welcome to EduGenie AI!",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "gemini_configured": client is not None
    }


@app.post("/qa")
def question_answer(request: LearningRequest):
    if not request.question.strip():
        raise HTTPException(400, "Please enter a question.")

    prompt = f"""
You are EduGenie, a friendly educational assistant.
Answer the student's question clearly and accurately.
Use simple language and examples when useful.

Student question: {request.question}
Student level: {request.level}
"""
    return {"answer": ask_gemini(prompt)}


@app.post("/explain")
def explain(request: LearningRequest):
    if not request.topic.strip():
        raise HTTPException(400, "Please enter a topic.")

    prompt = f"""
Explain this topic like a patient teacher.
Use a simple definition, key points, and one example.
Avoid unnecessary difficult words.

Topic: {request.topic}
Student level: {request.level}
"""
    return {"explanation": ask_gemini(prompt)}


@app.post("/quiz")
def quiz(request: LearningRequest):
    if not request.topic.strip():
        raise HTTPException(400, "Please enter a topic.")

    count = max(1, min(request.num_questions, 15))

    prompt = f"""
Create {count} multiple-choice quiz questions about:
{request.topic}

Student level: {request.level}

For each question, provide:
- The question
- Four options labeled A, B, C, D
- The correct answer
- A short explanation

Use clear formatting. Do not include unrelated questions.
"""
    return {"quiz": ask_gemini(prompt)}


@app.post("/summarize")
def summarize(request: LearningRequest):
    if not request.text.strip():
        raise HTTPException(400, "Please enter text to summarize.")

    prompt = f"""
Summarize the following study material.
Include a short overview and the most important points.
Use simple language and preserve the original meaning.

Text:
{request.text}
"""
    return {"summary": ask_gemini(prompt)}


@app.post("/learn/recommendations")
def recommendations(request: LearningRequest):
    subject = request.topic or request.question

    if not subject.strip():
        raise HTTPException(400, "Please enter a subject or topic.")

    prompt = f"""
Create a beginner-friendly learning path for:
{subject}

Include:
1. What to learn first
2. The next topics in order
3. A small practice activity for each stage
4. A short revision plan

Keep it practical and easy to follow.
"""
    return {"recommendations": ask_gemini(prompt)}