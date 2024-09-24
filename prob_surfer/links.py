from typing import Dict, Optional, Set

from .automata import ALL_AUTOMATAS

from .automata.execution import run_automaton_on_tree
from .db import XmlNodeDB


def _get_all_out_links(db: XmlNodeDB) -> Set[str]:
    # perform BFS
    link = db.get_link()
    curr_links: Set[str] = set()
    if link is not None:
        curr_links.add(link)
    for node in db.children:
        curr_links.update(_get_all_out_links(node))
    return curr_links


def get_out_links_probabilities(
    db: XmlNodeDB, strategy: str, automaton_str: Optional[str]
) -> Dict[str, float]:
    if strategy == "uniform":
        all_links = _get_all_out_links(db)
        if len(all_links) == 0:
            return {}
        prob_each = 1.0 / len(all_links)
        return {link: prob_each for link in all_links}
    elif strategy == "automaton":
        assert (
            automaton_str is not None
        ), "automaton specification is required when using strategy='automaton'"

        assert automaton_str in ALL_AUTOMATAS, (
            f"Got unknown automaton type {automaton_str}, "
            f"expected one of {list(ALL_AUTOMATAS.keys())}"
        )

        automaton = ALL_AUTOMATAS[automaton_str]()

        root_state = run_automaton_on_tree(db, automaton)
        return root_state.url_probas
    else:
        strategies = ["uniform", "automaton"]
        raise ValueError(
            f"out link strategy should be one of {strategies}, got {strategy}"
        )
