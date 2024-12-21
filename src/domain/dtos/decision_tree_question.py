from typing import NamedTuple


class DecisionTreeQuestion(NamedTuple):
    text: str
    yes_nodes: list[str]
    no_nodes: list[str]
