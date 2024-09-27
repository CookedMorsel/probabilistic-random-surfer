from typing import List
from prob_surfer.automata.automaton import AutomataNodeState, BottomUpTreeAutomaton
from prob_surfer.db import XmlNode


class LazyTop3Automaton(BottomUpTreeAutomaton):
    """
    Assumes the user is "lazy" and clicks on one of the top 3 links with 
    probabilities [0.5, 0.3, 0.2]. Links appearing further have probability 0.
    If the number of children is smaller then 3, normalizes the probabilities.
    For example, having 2 children means probabilities [0.5/0.8, 0.3/0.8] = [0.625, 0.375]
    Example:
        a
       / \ 
     /|\  b
    c d e
    Assuming b,c,d,e are links, the probabilities are:
    0.375               b
    0.5*0.625 = 0.3125  c
    0.3*0.625 = 0.1875  d
    0.2*0.625 = 0.125   e
    """

    def delta(
        self, node: XmlNode, children_states: List[AutomataNodeState]
    ) -> AutomataNodeState:
        non_empty_children_states = [
            state for state in children_states if len(state.url_probas) > 0
        ]
        n = len(non_empty_children_states)

        PROBAS = {1: 0.5, 2: 0.3, 3: 0.2}

        if n == 0:
            # Base case
            link = node.get_link()
            if link is None:
                url_probas = {}
            else:
                url_probas = {link: 1.0}

        else:
            url_probas = {}
            normalizer = sum(list(PROBAS.values())[: len(non_empty_children_states)])

            for child_idx, child_state in enumerate(non_empty_children_states, start=1):
                if child_idx > len(PROBAS):
                    break  # All other probabilities are 0
                base_multiplier = PROBAS[child_idx]

                for link, original_proba in child_state.url_probas.items():
                    if link not in url_probas:
                        url_probas[link] = 0.0

                    # Each child gets weight corresponding to the base_multiplier of its father.
                    # Normalize in case num of children < 3.
                    url_probas[link] += original_proba * base_multiplier / normalizer
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
