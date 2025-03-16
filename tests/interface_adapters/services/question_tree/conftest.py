from unittest.mock import MagicMock

import pytest

from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion, AnswerOption
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.history_manager import HistoryManager
from src.interface_adapters.services.question_tree.question_mapping_manager import QuestionsMappingManager
from src.interface_adapters.services.question_tree.tree_iterator import TreeIterator
from src.interface_adapters.services.question_tree.unvisited_queue import UnvisitedQueue


@pytest.fixture
def mock_page() -> Page[ResTukeStudyProgrammeData]:
    """Create a mock Page object."""
    mock_data = MagicMock(spec=ResTukeStudyProgrammeData)
    mock_data.name = "Test Programme"
    mock_page = MagicMock(spec=Page)
    mock_page.data = mock_data
    return mock_page


@pytest.fixture
def mock_binary_question(mock_page: Page[ResTukeStudyProgrammeData]) -> BinaryQuestion[Page[ResTukeStudyProgrammeData]]:
    """Create a mock BinaryQuestion."""
    return BinaryQuestion(
        text="Test binary question?",
        yes_answer_node=mock_page,
        no_answer_node=mock_page
    )


@pytest.fixture
def mock_options_question(mock_page: Page[ResTukeStudyProgrammeData]) -> OptionsQuestion[Page[ResTukeStudyProgrammeData]]:
    """Create a mock OptionsQuestion."""
    option1 = AnswerOption(text="Option 1", answer_node=mock_page)
    option2 = AnswerOption(text="Option 2", answer_node=mock_page)
    return OptionsQuestion(
        text="Test options question?",
        answer_options=[option1, option2]
    )


@pytest.fixture
def history_manager() -> HistoryManager:
    """Create a HistoryManager instance."""
    return HistoryManager()


@pytest.fixture
def unvisited_queue() -> UnvisitedQueue:
    """Create an UnvisitedQueue instance."""
    return UnvisitedQueue()


@pytest.fixture
def questions_mapping_manager() -> QuestionsMappingManager:
    """Create a QuestionsMappingManager instance."""
    return QuestionsMappingManager()


@pytest.fixture
def tree_iterator(
    history_manager: HistoryManager, 
    unvisited_queue: UnvisitedQueue, 
    questions_mapping_manager: QuestionsMappingManager
) -> TreeIterator:
    """Create a TreeIterator instance."""
    return TreeIterator(
        history=history_manager,
        queue=unvisited_queue,
        tree_mapping_manager=questions_mapping_manager
    )
