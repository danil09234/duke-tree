from pydantic import BaseModel


class CurrentQuestionResponse(BaseModel):
    question: str
    answers: list[str]
