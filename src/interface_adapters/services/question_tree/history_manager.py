from collections import OrderedDict
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData
from src.interface_adapters.gateways.study_programmes_gateway_base import Page
from loguru import logger


class HistoryManager:
    """
    Manages the history of answers and corresponding study programs.

    Keeps track of the user's navigation through the question tree and stores
    study programs found along the way.
    """

    def __init__(self) -> None:
        self._history: OrderedDict[str, list[Page[ResTukeStudyProgrammeData]]] = OrderedDict()

    def add_entry(self, node_id: int, answer: Page[ResTukeStudyProgrammeData]) -> None:
        """
        Add a new entry to the history.

        :param node_id: The ID of the question node
        :param answer: The answer
        """
        if str(node_id) not in self._history:
            self._history[str(node_id)] = [answer]
        else:
            self._history[str(node_id)].append(answer)

    def cancel_after_node(self, node_id: int) -> None:
        """
        Remove all history entries after the specified node.

        :param node_id: The ID of the node after which to cancel history
        """
        keys = list(self._history.keys())
        for key in keys:
            if int(key) >= node_id:
                del self._history[key]

    def get_results(self) -> list[Page[ResTukeStudyProgrammeData]]:
        """
        Get all study programs stored in the history.

        :return: List of pages containing study programme data
        """
        return [program for programs in self._history.values() for program in programs]
