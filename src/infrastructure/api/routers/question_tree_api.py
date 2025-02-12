from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from src.infrastructure.api.dependencies.question_tree_api_session import get_question_tree_api_session
from src.infrastructure.api.types.answer_request import AnswerRequest
from src.infrastructure.api.types.current_question_response import CurrentQuestionResponse
from src.infrastructure.api.types.study_programme_response import StudyProgrammeResponse
from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession

router = APIRouter()


@router.post("/session", response_model=str)
async def create_session(session_service: QuestionTreeAPISession = Depends(get_question_tree_api_session)) -> str:
    session_id = session_service.create_session()
    return session_id


@router.get("/session/{session_id}/question", response_model=CurrentQuestionResponse)
async def get_current_question(
        session_id: str,
        session_service: QuestionTreeAPISession = Depends(get_question_tree_api_session)
) -> CurrentQuestionResponse:
    try:
        current_question = session_service.get_current_question(session_id)
        return current_question
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found or completed")


@router.post("/session/{session_id}/answer", response_model=Optional[list[StudyProgrammeResponse]])
async def answer_question(
        session_id: str,
        answer_request: AnswerRequest,
        session_service: QuestionTreeAPISession = Depends(get_question_tree_api_session)
) -> Optional[list[StudyProgrammeResponse]]:
    try:
        result = session_service.answer_question(session_id, answer_request.answer)
        if result is not None:
            return [StudyProgrammeResponse(name=programme.data.name, code=programme.metadata.code) for programme in result]
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
