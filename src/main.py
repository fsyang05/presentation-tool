from schemas import QuestionSet
from fastapi import FastAPI
from services import generate_report

app = FastAPI()

@app.post("/")
async def entry(questions: QuestionSet):
    response = await generate_report(questions)
    return response