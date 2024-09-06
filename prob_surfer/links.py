from typing import Dict, Set
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


def get_out_links_probabilities(db: XmlNodeDB, strategy: str) -> Dict[str, float]:
    if strategy == "uniform":
        all_links = _get_all_out_links(db)
        prob_each = 1.0 / len(all_links)
        return {link: prob_each for link in all_links}
    elif strategy == "automata":
        raise NotImplementedError()
    else:
        strategies = ["uniform", "automata"]
        raise ValueError(
            f"out link strategy should be one of {strategies}, got {strategy}"
        )
