# EduGenie AI

## Google Gemini Powered Learning Assistant

EduGenie is an AI-based learning assistant
that helps students understand their subjects
using Google Gemini AI.

## Features

- Question and Answer
- Topic Explanation
- Quiz Generation
- Text Summarization
- Learning Recommendations

## Technologies Used

- Python
- FastAPI
- Google Gemini API
- HTML
- CSS

## Installation

Install the required packages:

pip install -r requirements.txt

## Run the Project

uvicorn main:app --reload

## API Documentation

After running the project, open:

http://127.0.0.1:8000/docs

## API Endpoints

- GET /
- GET /health
- POST /qa
- POST /explain
- POST /quiz
- POST /summarize
- POST /learn/recommendations

## API Configuration

Create a .env file on your computer.

Add your Gemini API key:

GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.5-flash

Do not upload your .env file to GitHub.

## Project

EduGenie AI - Student Learning Assistant