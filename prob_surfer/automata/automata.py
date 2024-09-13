from abc import abstractmethod
from typing import List

from ..db import XmlNode


class AutomataNodeState:
    q: str


class BottomUpTreeAutomata:
    """
    Defines a non-deterministic bottom up tree automata
    """

    @abstractmethod
    def delta(
        node: XmlNode, children_states: List[AutomataNodeState]
    ) -> List[AutomataNodeState]:
        """
        Defines non-deterministic transition rules for node states.
        The returned list contains all the possible transitions,
        with one of them being chosen at random.
        """
        raise NotImplementedError()
