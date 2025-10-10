from pydantic import BaseModel

class Question(BaseModel):
    question: str
    answer: str

class QuestionSet(BaseModel):
    id: int
    sets: list[Question]
