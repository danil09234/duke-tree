from pydantic import BaseModel


class AnswerRequest(BaseModel):
    answer_token: str
