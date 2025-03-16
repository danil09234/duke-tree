from collections import OrderedDict
from loguru import logger

from src.interface_adapters.services.question_tree.type_aliases import QuestionNode


class UnvisitedQueue:
    """
    Manages a queue of unvisited nodes in the question tree.

    Maintains a mapping of parent nodes to their unvisited children.
    """

    def __init__(self) -> None:
        """
        Initialize a new UnvisitedQueue
        """
        self._queue: OrderedDict[int, list[QuestionNode]] = OrderedDict()
        logger.debug("Initialized new UnvisitedQueue")

    def add_node_to_visit(self, parent_node_id: int, node: QuestionNode) -> None:
        """
        Add a node to the unvisited queue.

        :param parent_node_id: ID of the parent node
        :param node: The question node to be visited later
        """
        if parent_node_id not in self._queue:
            self._queue[parent_node_id] = []
        self._queue[parent_node_id].append(node)
        logger.debug(f"Added node {parent_node_id} to queue")

    def pop_next(self) -> QuestionNode | None:
        """
        Get and remove the next unvisited node from the queue.

        :return: The next question node to visit, or None if queue is empty
        """
        if not self._queue:
            logger.debug("Queue is empty")
            return None
        first_key = next(iter(self._queue))
        nodes = self._queue[first_key]
        if not nodes:
            del self._queue[first_key]
            return self.pop_next()
        next_node = nodes.pop(0)
        if not nodes:
            del self._queue[first_key]
        logger.debug(f"Popped node, queue size: {len(self._queue)}")
        return next_node

    def clear_from_key(self, key: int) -> None:
        """
        Clear all unvisited nodes after the specified key.

        :param key: The key after which to clear nodes
        """
        logger.debug(f"Clearing queue from key: {key} onwards")
        keys_to_delete = [k for k in self._queue.keys() if k >= key]
        for k in keys_to_delete:
            del self._queue[k]
        logger.debug(f"Queue size after clearing: {len(self._queue)}")

    def is_empty(self) -> bool:
        """
        Check if the unvisited queue is empty.

        :return: True if queue is empty, False otherwise
        """
        return len(self._queue) == 0