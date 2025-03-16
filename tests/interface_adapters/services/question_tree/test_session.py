from src.domain.entities.binary_question import BinaryQuestion
from src.domain.entities.options_question import OptionsQuestion
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.session import Session


def test_init_with_binary_question(mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test initialization with a binary question."""
    session = Session(mock_binary_question)
    current_node = session.get_current_node()
    
    assert current_node.question == mock_binary_question.text
    assert len(current_node.answers) == 3
    assert "yes" in current_node.answers.values()
    assert "no" in current_node.answers.values()
    assert "probably" in current_node.answers.values()


def test_init_with_options_question(mock_options_question: OptionsQuestion[Page[ResTukeStudyProgrammeData]]) -> None:
    """Test initialization with an options question."""
    session = Session(mock_options_question)
    current_node = session.get_current_node()
    
    assert current_node.question == mock_options_question.text
    assert len(current_node.answers) == 2
    assert "Option 1" in current_node.answers.values()
    assert "Option 2" in current_node.answers.values()


def test_set_answer_binary_question(
    mock_binary_question: BinaryQuestion[Page[ResTukeStudyProgrammeData]], 
    mock_page: Page[ResTukeStudyProgrammeData]
) -> None:
    """Test setting an answer for a binary question."""
    session = Session(mock_binary_question)
    current_node = session.get_current_node()

    yes_token = [token for token, value in current_node.answers.items() if value == "yes"][0]

    result = session.set_answer(yes_token)
    assert result == [mock_page]


def test_set_answer_options_question(
    mock_options_question: OptionsQuestion[Page[ResTukeStudyProgrammeData]], 
    mock_page: Page[ResTukeStudyProgrammeData]
) -> None:
    """Test setting an answer for an options question."""
    session = Session(mock_options_question)
    current_node = session.get_current_node()

    option_token = [token for token, value in current_node.answers.items() if value == "Option 1"][0]

    result = session.set_answer(option_token)
    assert result == [mock_page]
