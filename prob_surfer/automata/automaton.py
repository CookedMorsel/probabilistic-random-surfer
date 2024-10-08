from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Dict, List

from ..db import XmlNode


@dataclass
class AutomataNodeState:
    url_probas: Dict[str, float]


class BottomUpTreeAutomaton(ABC):
    """
    Defines a non-deterministic bottom up tree automaton
    """

    @abstractmethod
    def delta(
        self, node: XmlNode, children_states: List[AutomataNodeState]
    ) -> AutomataNodeState:
        """
        Defines non-deterministic transition rules for node states.
        """
        raise NotImplementedError()
