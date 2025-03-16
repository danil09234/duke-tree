from unittest.mock import MagicMock

import pytest

from src.domain.entities.question_tree import QuestionTree
from src.interface_adapters.services.question_tree.exceptions import SessionNotFoundError
from src.interface_adapters.services.question_tree.session_manager import SessionManager


def test_init() -> None:
    """Test initialization of SessionManager."""
    mock_tree = MagicMock(spec=QuestionTree)
    manager = SessionManager(mock_tree)
    assert isinstance(manager, SessionManager)


def test_create_session() -> None:
    """Test creating a new session."""
    mock_tree = MagicMock(spec=QuestionTree)
    mock_tree.root = MagicMock()
    
    manager = SessionManager(mock_tree)
    session_id = manager.create_session()
    
    assert isinstance(session_id, str)
    assert len(session_id) > 0


def test_get_session_exists() -> None:
    """Test getting an existing session."""
    mock_tree = MagicMock(spec=QuestionTree)
    mock_tree.root = MagicMock()
    
    manager = SessionManager(mock_tree)
    session_id = manager.create_session()
    
    session = manager.get_session(session_id)
    assert session is not None


def test_get_session_not_found() -> None:
    """Test exception is raised when session is not found."""
    mock_tree = MagicMock(spec=QuestionTree)
    manager = SessionManager(mock_tree)
    
    with pytest.raises(SessionNotFoundError):
        manager.get_session("non_existent_session")


def test_generate_session_id() -> None:
    """Test session ID generation produces unique IDs."""
    mock_tree = MagicMock(spec=QuestionTree)
    manager = SessionManager(mock_tree)
    
    session_id1 = manager._generate_session_id()
    session_id2 = manager._generate_session_id()
    
    assert session_id1 != session_id2
