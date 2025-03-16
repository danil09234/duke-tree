import pytest

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.exceptions import AnswerTokenNotFound
from src.interface_adapters.services.question_tree.question_mapping_manager import QuestionsMappingManager


def test_init() -> None:
    """Test initialization of QuestionsMappingManager."""
    manager = QuestionsMappingManager()
    assert isinstance(manager, QuestionsMappingManager)


def test_add_node(mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test adding a node to the mapping."""
    manager = QuestionsMappingManager()
    node_id = manager.add_node(mock_binary_question)
    assert node_id == 1
    
    retrieved_node = manager.get_node_by_id(node_id)
    assert retrieved_node == mock_binary_question


def test_add_answer_option(mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test adding an answer option for a node."""
    manager = QuestionsMappingManager()
    node_id = manager.add_node(mock_binary_question)
    
    answer_token = manager.add_answer_option(node_id, "yes")
    assert isinstance(answer_token, str)

    retrieved_node_id = manager.get_node_id_by_answer_token(answer_token)
    assert retrieved_node_id == node_id

    answer_value = manager.get_answer_value_by_token(answer_token)
    assert answer_value == "yes"


def test_get_node_id_by_answer_token_not_found() -> None:
    """Test exception is raised when answer token is not found."""
    manager = QuestionsMappingManager()
    
    with pytest.raises(AnswerTokenNotFound):
        manager.get_node_id_by_answer_token("non_existent_token")


def test_get_current_node(mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test getting the current (last added) node."""
    manager = QuestionsMappingManager()
    node_id = manager.add_node(mock_binary_question)
    manager.add_answer_option(node_id, "yes")
    manager.add_answer_option(node_id, "no")
    
    current_node = manager.get_current_node()
    assert current_node.question == mock_binary_question.text
    assert len(current_node.answers) == 2
    assert "yes" in current_node.answers.values()
    assert "no" in current_node.answers.values()


def test_clear_from_node_id(
    mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]], 
    mock_options_question: OptionsQuestion[Page[ResTukeStudyProgrammeData]]
) -> None:
    """Test clearing mappings after a specific node ID."""
    manager = QuestionsMappingManager()

    node_id1 = manager.add_node(mock_binary_question)
    token1 = manager.add_answer_option(node_id1, "yes")
    token2 = manager.add_answer_option(node_id1, "no")

    node_id2 = manager.add_node(mock_options_question)
    token3 = manager.add_answer_option(node_id2, "Option 1")

    manager.clear_from_node_id(node_id1)

    assert manager.get_node_by_id(node_id1) == mock_binary_question
    assert manager.get_answer_value_by_token(token1) == "yes"
    assert manager.get_answer_value_by_token(token2) == "no"

    with pytest.raises(KeyError):
        manager.get_node_by_id(node_id2)
    
    with pytest.raises(KeyError):
        manager.get_answer_value_by_token(token3)
