from services.llm.openai import OpenAIClient
from schemas import QuestionSet
from pathlib import Path
from services.utils import generate_presentation_pdf
from services.utils import send_presentation_email

client = OpenAIClient()

async def generate_report(data: QuestionSet):
    all_questions = ""
    for q in data.sets:
        all_questions += f"question: {q.question}\nanswer: {q.answer}\n"

    res = client.generate_response(all_questions)
    if not res["success"]:
        return None

    await generate_presentation_pdf(res["data"], Path("presentation.pdf"))

    # wip
    #await send_presentation_email("felixyang2028@u.northwestern.edu")

    return res["data"]