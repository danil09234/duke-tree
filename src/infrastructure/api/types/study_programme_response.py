from pydantic import BaseModel


class StudyProgrammeResponse(BaseModel):
    study_programme_code: str
