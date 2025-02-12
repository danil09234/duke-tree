import pytest
from uuid import UUID

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.entities.question_tree import QuestionTree
from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession
from src.interface_adapters.gateways.study_programmes_gateway_base import Page


def test_create_session_binary(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    UUID(session_id)
    assert session_id in session.sessions
    assert isinstance(session.sessions[session_id].current_node, BinaryQuestion)


def test_get_current_question_binary(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    resp = session.get_current_question(session_id)

    assert resp.question == "Are you interested in computer technologies?"
    assert resp.answers == ["Yes", "No", "Combined"]


def test_get_current_question_options(options_transitions_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(options_transitions_tree)
    session_id = session.create_session()
    resp = session.get_current_question(session_id)
    expected = ["Yes", "No", "Combined"]
    assert resp.question == "Do you like programming?"
    assert sorted(resp.answers) == sorted(expected)


def test_answer_binary_question(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "Yes")

    assert result is not None
    assert result[0].data.name == "Programme 1 EN"
    assert session_id not in session.sessions


def test_answer_binary_question_intermediate(complex_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(complex_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "No")
    assert result is None
    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in quality management?"


def test_answer_options_question(options_transitions_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(options_transitions_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "Yes")

    assert result is not None
    assert result[0].data.name == "Programme 1 EN"
    assert session_id not in session.sessions


def test_answer_complex_path(full_generation_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(full_generation_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "Practical")
    assert result is None
    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in computer technologies?"
    result = session.answer_question(session_id, "No")
    assert result is None
    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in quality management?"
    result = session.answer_question(session_id, "Yes")

    assert result is not None
    assert result[0].data.name == "Programme 3 EN"
    assert session_id not in session.sessions


def test_answer_binary_question_combined(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "Combined")

    assert isinstance(result, list)
    assert result[0].data.name == "Programme 1 EN"
    assert result[1].data.name == "Programme 2 EN"


def test_answer_options_question_combined(
        options_transitions_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(options_transitions_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "Combined")

    assert isinstance(result, list)
    assert result[0].data.name == "Programme 1 EN"
    assert result[1].data.name == "Programme 2 EN"


def test_get_current_question_invalid_session(
        simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    with pytest.raises(ValueError, match="Session not found"):
        session.get_current_question("non-existent")


def test_answer_question_invalid_session(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    with pytest.raises(ValueError, match="Session not found"):
        session.answer_question("non-existent", "Yes")


def test_answer_question_invalid_binary_answer(
        simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    with pytest.raises(ValueError, match="Answer must be 'yes', 'no' or 'combined'"):
        session.answer_question(session_id, "invalid")


def test_answer_question_invalid_option(
        options_transitions_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(options_transitions_tree)
    session_id = session.create_session()
    with pytest.raises(ValueError, match="Invalid answer option"):
        session.answer_question(session_id, "invalid")
