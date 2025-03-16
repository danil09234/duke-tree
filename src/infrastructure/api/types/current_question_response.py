from pydantic import BaseModel


class CurrentQuestionResponse(BaseModel):
    question: str
    answers: dict[str, str]  # token -> answer text
