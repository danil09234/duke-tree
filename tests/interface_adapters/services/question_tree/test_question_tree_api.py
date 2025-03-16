from typing import List
from unittest.mock import MagicMock

import pytest

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.api import QuestionTreeAPI
from src.interface_adapters.services.question_tree.exceptions import SessionNotFoundError


def test_init() -> None:
    """Test initialization of QuestionTreeAPI."""
    mock_tree = MagicMock(spec=QuestionTree)
    api = QuestionTreeAPI(mock_tree)
    assert isinstance(api, QuestionTreeAPI)


def test_create_session() -> None:
    """Test creating a new session through the API."""
    mock_tree = MagicMock(spec=QuestionTree)
    mock_tree.root = MagicMock()
    
    api = QuestionTreeAPI(mock_tree)
    session_id = api.create_session()
    
    assert isinstance(session_id, str)
    assert len(session_id) > 0


def test_get_current_question() -> None:
    """Test getting the current question for a session."""
    mock_binary_question = MagicMock(spec=BinaryQuestion)
    mock_binary_question.text = "Test question"
    
    mock_tree = MagicMock(spec=QuestionTree)
    mock_tree.root = mock_binary_question
    
    api = QuestionTreeAPI(mock_tree)
    session_id = api.create_session()
    
    current_question = api.get_current_question(session_id)
    assert current_question is not None
    assert hasattr(current_question, 'question')
    assert hasattr(current_question, 'answers')


def test_answer_question() -> None:
    """Test answering a question through the API."""
    mock_session = MagicMock()
    mock_result: List[Page[ResTukeStudyProgrammeData]] = [MagicMock()]
    mock_session.set_answer.return_value = mock_result

    mock_session_manager = MagicMock()
    mock_session_manager.get_session.return_value = mock_session
    mock_session_manager.create_session.return_value = "test_session_id"

    mock_tree = MagicMock(spec=QuestionTree)
    api = QuestionTreeAPI(mock_tree)
    api._session_manager = mock_session_manager
    
    # Test answering a question
    result = api.answer_question("test_session_id", "test_answer")
    assert result == mock_result
    mock_session.set_answer.assert_called_once_with("test_answer")


def test_get_current_question_session_not_found() -> None:
    """Test exception is raised when session is not found for get_current_question."""
    mock_tree = MagicMock(spec=QuestionTree)
    api = QuestionTreeAPI(mock_tree)

    mock_session_manager = MagicMock()
    mock_session_manager.get_session.side_effect = SessionNotFoundError("Session not found")
    api._session_manager = mock_session_manager
    
    with pytest.raises(SessionNotFoundError):
        api.get_current_question("non_existent_session")


def test_answer_question_session_not_found() -> None:
    """Test exception is raised when session is not found for answer_question."""
    mock_tree = MagicMock(spec=QuestionTree)
    api = QuestionTreeAPI(mock_tree)

    mock_session_manager = MagicMock()
    mock_session_manager.get_session.side_effect = SessionNotFoundError("Session not found")
    api._session_manager = mock_session_manager
    
    with pytest.raises(SessionNotFoundError):
        api.answer_question("non_existent_session", "test_answer")
