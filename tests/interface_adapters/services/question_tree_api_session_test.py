from uuid import UUID

import pytest

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.question_tree import QuestionTree
from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession


@pytest.fixture
def api_session(request: pytest.FixtureRequest) -> QuestionTreeAPISession:
    tree = request.getfixturevalue(request.param)
    return QuestionTreeAPISession(tree)


@pytest.mark.parametrize('api_session', ['simple_binary_tree'], indirect=True)
def test_create_session(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()

    UUID(session_id)
    assert session_id in api_session.sessions
    assert isinstance(api_session.sessions[session_id].current_node, BinaryQuestion)


@pytest.mark.parametrize('api_session', ['simple_binary_tree'], indirect=True)
def test_get_current_question_binary(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()
    
    question = api_session.get_current_question(session_id)
    assert question.question == "Are you interested in computer technologies?"
    assert question.answers == ["Yes", "No"]


@pytest.mark.parametrize('api_session', ['options_transitions_tree'], indirect=True)
def test_get_current_question_options(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()
    
    question = api_session.get_current_question(session_id)
    assert question.question == "Do you like programming?"
    assert len(question.answers) == 2
    assert "Yes" in question.answers
    assert "No" in question.answers


@pytest.mark.parametrize('api_session', ['simple_binary_tree'], indirect=True)
def test_answer_binary_question(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()
    
    result = api_session.answer_question(session_id, "Yes")
    assert result is not None
    assert result.data.name == "Programme 1 EN"
    assert session_id not in api_session.sessions


@pytest.mark.parametrize('api_session', ['complex_tree'], indirect=True)
def test_answer_binary_question_intermediate(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()

    result = api_session.answer_question(session_id, "No")

    assert result is None
    assert session_id in api_session.sessions

    question = api_session.get_current_question(session_id)
    assert question.question == "Are you interested in quality management?"


@pytest.mark.parametrize('api_session', ['options_transitions_tree'], indirect=True)
def test_answer_options_question(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()
    
    result = api_session.answer_question(session_id, "Yes")
    assert result is not None
    assert result.data.name == "Programme 1 EN"
    assert session_id not in api_session.sessions


@pytest.mark.parametrize('api_session', ['full_generation_tree'], indirect=True)
def test_answer_complex_path(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()

    result = api_session.answer_question(session_id, "Practical")
    assert result is None
    assert isinstance(api_session.sessions[session_id].current_node, BinaryQuestion)

    result = api_session.answer_question(session_id, "No")
    assert result is None
    assert isinstance(api_session.sessions[session_id].current_node, BinaryQuestion)

    result = api_session.answer_question(session_id, "Yes")
    assert result is not None
    assert result.data.name == "Programme 3 EN"
    assert session_id not in api_session.sessions


def test_get_current_question_invalid_session() -> None:
    session = QuestionTreeAPISession(QuestionTree(root=BinaryQuestion("test", None, None)))  # type: ignore
    with pytest.raises(ValueError, match="Session not found"):
        session.get_current_question("invalid-session")


def test_answer_question_invalid_session() -> None:
    session = QuestionTreeAPISession(QuestionTree(root=BinaryQuestion("test", None, None)))  # type: ignore
    with pytest.raises(ValueError, match="Session not found"):
        session.answer_question("invalid-session", "Yes")


@pytest.mark.parametrize('api_session', ['simple_binary_tree'], indirect=True)
def test_answer_question_invalid_binary_answer(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()
    
    with pytest.raises(ValueError, match="Answer must be 'yes' or 'no'"):
        api_session.answer_question(session_id, "Maybe")


@pytest.mark.parametrize('api_session', ['options_transitions_tree'], indirect=True)
def test_answer_question_invalid_option(api_session: QuestionTreeAPISession) -> None:
    session_id = api_session.create_session()
    
    with pytest.raises(ValueError, match="Invalid answer option"):
        api_session.answer_question(session_id, "Invalid")