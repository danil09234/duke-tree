import pytest
from uuid import UUID

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion, AnswerOption
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.domain.entities.question_tree import QuestionTree
from src.interface_adapters.services.question_tree_api_session import QuestionTreeAPISession
from src.interface_adapters.gateways.study_programmes_gateway_base import Page


def test_create_session_binary(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    UUID(session_id)
    assert session_id in session._sessions
    assert isinstance(session._sessions[session_id]._current_node, BinaryQuestion)


def test_get_current_question_binary(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    resp = session.get_current_question(session_id)

    assert resp.question == "Are you interested in computer technologies?"
    assert resp.answers == ["Yes", "No", "Probably"]


def test_get_current_question_options(options_transitions_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(options_transitions_tree)
    session_id = session.create_session()
    resp = session.get_current_question(session_id)
    expected = ["Yes", "No"]
    assert resp.question == "Do you like programming?"
    assert sorted(resp.answers) == sorted(expected)


def test_answer_binary_question(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "Yes")

    assert result is not None
    assert result[0].data.name == "Programme 1 EN"
    assert session_id not in session._sessions


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
    assert session_id not in session._sessions


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
    assert session_id not in session._sessions


def test_answer_binary_question_combined(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(simple_binary_tree)
    session_id = session.create_session()
    result = session.answer_question(session_id, "Probably")

    assert isinstance(result, list)
    assert result[0].data.name == "Programme 1 EN"
    assert result[1].data.name == "Programme 2 EN"


def test_answer_options_question_all_results(options_transitions_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session1 = QuestionTreeAPISession(options_transitions_tree)
    session_id1 = session1.create_session()
    result1 = session1.answer_question(session_id1, "Yes")

    session2 = QuestionTreeAPISession(options_transitions_tree)
    session_id2 = session2.create_session()
    result2 = session2.answer_question(session_id2, "No")

    assert result1 is not None
    assert result2 is not None
    assert result1[0].data.name == "Programme 1 EN"
    assert result2[0].data.name == "Programme 2 EN"


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
    with pytest.raises(ValueError, match="Answer must be 'yes', 'no' or 'probably'"):
        session.answer_question(session_id, "invalid")


def test_answer_question_invalid_option(
        options_transitions_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    session = QuestionTreeAPISession(options_transitions_tree)
    session_id = session.create_session()
    with pytest.raises(ValueError, match="Invalid answer option"):
        session.answer_question(session_id, "invalid")


# Tests for session history tracking and reset functionality
def test_session_history_tracking(complex_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test that history is correctly tracked while answering questions."""
    session = QuestionTreeAPISession(complex_tree)
    session_id = session.create_session()

    result = session.answer_question(session_id, "No")
    assert result is None

    history = session.get_session_history(session_id)
    assert len(history) == 1
    assert history[0]["question"] == "Are you interested in computer technologies?"
    assert history[0]["answer"] == "No"
    assert "node_id" in history[0]
    
    result = session.answer_question(session_id, "Yes")
    
    history = session.get_session_history(session_id)
    assert len(history) == 2
    assert history[1]["question"] == "Are you interested in quality management?"
    assert history[1]["answer"] == "Yes"


def test_reset_to_node(complex_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test resetting a session to a previous question node."""
    session = QuestionTreeAPISession(complex_tree)
    session_id = session.create_session()

    result = session.answer_question(session_id, "No")
    assert result is None

    history = session.get_session_history(session_id)
    first_node_id = history[0]["node_id"]
    
    # Answer second question
    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in quality management?"

    session.reset_to_node(session_id, first_node_id)

    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in computer technologies?"

    history = session.get_session_history(session_id)
    assert len(history) == 1
    assert history[0]["node_id"] == first_node_id


def test_reset_invalid_node_id(complex_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test that resetting with an invalid node ID raises an error."""
    session = QuestionTreeAPISession(complex_tree)
    session_id = session.create_session()

    with pytest.raises(ValueError, match="Node ID .* not found"):
        session.reset_to_node(session_id, "non-existent-node-id")


def test_restart_after_reset(complex_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test that answering after a reset works correctly and follows a different path."""
    session = QuestionTreeAPISession(complex_tree)
    session_id = session.create_session()

    result = session.answer_question(session_id, "No")
    assert result is None

    history = session.get_session_history(session_id)
    first_node_id = history[0]["node_id"]

    session.reset_to_node(session_id, first_node_id)

    result = session.answer_question(session_id, "Yes")
    assert result is not None

    assert result[0].data.name == "Programme 1 EN"


def test_get_session_history_invalid_session(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test that trying to get history for an invalid session raises an error."""
    session = QuestionTreeAPISession(simple_binary_tree)
    with pytest.raises(ValueError, match="Session not found"):
        session.get_session_history("non-existent")


def test_reset_session_invalid_session(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test that trying to reset an invalid session raises an error."""
    session = QuestionTreeAPISession(simple_binary_tree)
    with pytest.raises(ValueError, match="Session not found"):
        session.reset_to_node("non-existent", "some-node-id")


def test_reset_and_continue_with_complex_path(test_study_programmes: list[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test resetting during a complex multi-step path and then continuing with different answers."""
    comp_tech_question = BinaryQuestion[Page[ResTukeStudyProgrammeData]](
        text="Are you interested in computer technologies?",
        yes_answer_node=test_study_programmes[0],
        no_answer_node=BinaryQuestion[Page[ResTukeStudyProgrammeData]](
            text="Are you interested in quality management?",
            yes_answer_node=test_study_programmes[2],
            no_answer_node=test_study_programmes[1]
        )
    )
    
    options = [
        AnswerOption[Page[ResTukeStudyProgrammeData]](
            text="Practical",
            answer_node=comp_tech_question
        ),
        AnswerOption[Page[ResTukeStudyProgrammeData]](
            text="Theoretical",
            answer_node=test_study_programmes[1]
        )
    ]
    
    root = OptionsQuestion[Page[ResTukeStudyProgrammeData]](
        text="What kind of study are you looking for?",
        answer_options=options
    )
    
    tree = QuestionTree[Page[ResTukeStudyProgrammeData]](root=root)

    session = QuestionTreeAPISession(tree)
    session_id = session.create_session()

    result = session.answer_question(session_id, "Practical")
    assert result is None

    comp_tech_history = session.get_session_history(session_id)
    comp_tech_id = comp_tech_history[0]["node_id"]

    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in computer technologies?"

    result = session.answer_question(session_id, "No")
    assert result is None

    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in quality management?"

    session.reset_to_node(session_id, comp_tech_id)

    resp = session.get_current_question(session_id)
    assert resp.question == "Are you interested in computer technologies?"

    result = session.answer_question(session_id, "Yes")

    assert result is not None
    assert result[0].data.name == "Programme 1 EN"