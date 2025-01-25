from pydantic import BaseModel


class StudyProgrammeResponse(BaseModel):
    name: str
    code: str
