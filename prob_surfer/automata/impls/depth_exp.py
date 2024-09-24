from typing import List
from prob_surfer.automata.automaton import AutomataNodeState, BottomUpTreeAutomaton
from prob_surfer.db import XmlNode


class ExponentialDepthAutomaton(BottomUpTreeAutomaton):
    """
    Gives links an exponential probability, by their depth in the XML DB.
    The divisor at each step is determined by the number of child nodes.
    Example:
        a
       / \ 
     /|\  b
    c d e
    Assuming b,c,d,e are links, the probabilities are:
    0.5  b
    0.166 c
    0.166 d
    0.166 e
    """

    def delta(
        self, node: XmlNode, children_states: List[AutomataNodeState]
    ) -> AutomataNodeState:
        non_empty_children_states = [
            state for state in children_states if len(state.url_probas) > 0
        ]
        n = len(non_empty_children_states)

        if n == 0:
            # Base case
            link = node.get_link()
            if link is None:
                url_probas = {}
            else:
                url_probas = {link: 1.0}

        else:
            url_probas = {}

            for child_state in non_empty_children_states:
                for link, proba in child_state.url_probas.items():
                    if link not in url_probas:
                        url_probas[link] = 0.0
                    url_probas[link] += proba / n  # Each child gets weight 1/n
                    # Important to perform addition instead of assignment in case the same link
                    # appears in multiple children

        if len(url_probas) > 0:
            # This check is highly recommended when implementing your own
            # automaton, to avoid implementation bugs
            assert (
                # round to avoid numeric errors
                round(sum(url_probas.values()), 6)
                == 1.0
            ), f"bugged computation: {sum(url_probas.values())}, {url_probas}"
        return AutomataNodeState(url_probas)
