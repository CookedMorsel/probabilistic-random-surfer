from ..db import XmlNodeDB
from .automaton import BottomUpTreeAutomaton, AutomataNodeState


def run_automaton_on_tree(
    root: XmlNodeDB, automaton: BottomUpTreeAutomaton
) -> AutomataNodeState:
    """
    Runs the supplied automaton on the given XML DB.
    Returns the final state of the root.
    """
    children_states = [
        run_automaton_on_tree(child, automaton) for child in root.children
    ]

    return automaton.delta(root.node, children_states)
