import logging
from typing import Optional

from prob_surfer.parsing.html import get_url_data_as_html
from prob_surfer.parsing.xml import html_data_as_xml_db
from .db import XmlNodeDB

logger = logging.getLogger(__name__)


def _print_node(node: XmlNodeDB, curr_depth: int):
    prefix = "  " * curr_depth
    num_children = len(node.children)
    print(
        f"{prefix}{node.node.tag: >10} | {num_children:>4} children | "
        f"{len(node.node.text):>6} len text | {len(node.node.attributes):>2} attributes"
    )


def print_tree(root: XmlNodeDB, curr_depth: int = 0, maxdepth: Optional[int] = None):
    if maxdepth is not None and curr_depth > maxdepth:
        return

    _print_node(root, curr_depth)
    for node in root.children:
        print_tree(node, curr_depth + 1)


def get_url_as_xml_db(url: str, xpath_filter: Optional[str] = None) -> XmlNodeDB:
    html_data = get_url_data_as_html(url)
    xml_db = html_data_as_xml_db(html_data, xpath_filter=xpath_filter)
    return xml_db
