from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from src.interface_adapters.services.question_tree.history_manager import HistoryManager


def test_init() -> None:
    """Test initialization of HistoryManager."""
    manager = HistoryManager()
    assert manager.get_results() == []


def test_add_entry(mock_page: Page[ResTukeStudyProgrammeData]) -> None:
    """Test adding an entry to the history."""
    manager = HistoryManager()
    manager.add_entry(1, mock_page)
    results = manager.get_results()
    assert len(results) == 1
    assert results[0] == mock_page


def test_add_multiple_entries(mock_page: Page[ResTukeStudyProgrammeData]) -> None:
    """Test adding multiple entries to the history."""
    manager = HistoryManager()
    manager.add_entry(1, mock_page)
    manager.add_entry(1, mock_page)
    manager.add_entry(2, mock_page)
    
    results = manager.get_results()
    assert len(results) == 3
    assert all(result == mock_page for result in results)


def test_cancel_after_node(mock_page: Page[ResTukeStudyProgrammeData]) -> None:
    """Test cancelling history after a specific node."""
    manager = HistoryManager()

    manager.add_entry(1, mock_page)
    manager.add_entry(2, mock_page)
    manager.add_entry(3, mock_page)

    manager.cancel_after_node(2)

    results = manager.get_results()
    assert len(results) == 1
