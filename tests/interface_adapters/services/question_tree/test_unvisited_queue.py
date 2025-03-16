from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.unvisited_queue import UnvisitedQueue


def test_init() -> None:
    """Test initialization of UnvisitedQueue."""
    queue = UnvisitedQueue()
    assert queue.is_empty() is True


def test_add_and_pop_node(mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test adding a node and then popping it."""
    queue = UnvisitedQueue()
    queue.add_node_to_visit(1, mock_binary_question)
    assert queue.is_empty() is False
    
    node = queue.pop_next()
    assert node == mock_binary_question
    assert queue.is_empty() is True


def test_multiple_nodes_same_parent(
    mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]],
    mock_options_question: OptionsQuestion[Page[ResTukeStudyProgrammeData]]
) -> None:
    """Test adding multiple nodes with the same parent."""
    queue = UnvisitedQueue()
    parent_id = 1
    
    queue.add_node_to_visit(parent_id, mock_binary_question)
    queue.add_node_to_visit(parent_id, mock_options_question)
    
    assert queue.is_empty() is False
    
    node1 = queue.pop_next()
    assert node1 == mock_binary_question
    
    node2 = queue.pop_next()
    assert node2 == mock_options_question
    
    assert queue.is_empty() is True


def test_multiple_nodes_different_parents(
    mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]],
    mock_options_question: OptionsQuestion[Page[ResTukeStudyProgrammeData]]
) -> None:
    """Test adding nodes with different parents."""
    queue = UnvisitedQueue()
    
    queue.add_node_to_visit(1, mock_binary_question)
    queue.add_node_to_visit(2, mock_options_question)
    
    assert queue.is_empty() is False

    node1 = queue.pop_next()
    assert node1 == mock_binary_question
    
    node2 = queue.pop_next()
    assert node2 == mock_options_question
    
    assert queue.is_empty() is True


def test_clear_from_key(
    mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]],
    mock_options_question: OptionsQuestion[Page[ResTukeStudyProgrammeData]]
) -> None:
    """Test clearing nodes from a specific key onwards."""
    queue = UnvisitedQueue()
    
    queue.add_node_to_visit(1, mock_binary_question)
    queue.add_node_to_visit(2, mock_options_question)
    queue.add_node_to_visit(3, mock_binary_question)
    
    queue.clear_from_key(2)

    assert queue.is_empty() is False
    node = queue.pop_next()
    assert node == mock_binary_question
    assert queue.is_empty() is True


def test_empty_queue_pop() -> None:
    """Test popping from an empty queue."""
    queue = UnvisitedQueue()
    assert queue.pop_next() is None
