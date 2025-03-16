import pytest

from src.domain.entities.question_tree import QuestionTree
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.api import QuestionTreeAPI


@pytest.mark.parametrize('tree_fixture', ['simple_binary_tree', 'complex_tree', 'options_transitions_tree', 'full_generation_tree'])
def test_question_tree_api_integration(request: pytest.FixtureRequest, tree_fixture: str) -> None:
    """Test end-to-end integration of QuestionTreeAPI with different tree structures."""
    tree = request.getfixturevalue(tree_fixture)
    api = QuestionTreeAPI(tree)

    session_id = api.create_session()
    assert isinstance(session_id, str)

    current_question = api.get_current_question(session_id)
    assert current_question.question is not None
    assert current_question.answers is not None
    assert len(current_question.answers) > 0

    first_answer_token = list(current_question.answers.keys())[0]
    result = api.answer_question(session_id, first_answer_token)

    assert result is None or isinstance(result, list)


def test_full_conversation_flow(simple_binary_tree: QuestionTree[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test a complete conversation flow through the API."""
    api = QuestionTreeAPI(simple_binary_tree)

    session_id = api.create_session()

    current_question = api.get_current_question(session_id)

    yes_token = [token for token, value in current_question.answers.items() if value == "yes"][0]

    result = api.answer_question(session_id, yes_token)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
