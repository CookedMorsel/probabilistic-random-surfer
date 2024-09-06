from typing import Optional
from lxml import html, etree  # type: ignore
import logging
from ..db import XmlNodeDB

logger = logging.getLogger(__name__)


def lxml_tree_to_xml_str(root) -> str:
    xml_content = etree.tostring(root, pretty_print=True, encoding="unicode")

    return xml_content


def html_data_as_lxml_tree(html_data: str) -> XmlNodeDB:
    try:
        root = html.fromstring(html_data)
    except Exception as e:
        raise ValueError("Failed converting html data to xml!") from e
    return root


def html_data_as_xml_db(html_data: str) -> XmlNodeDB:
    """
    Converts HTML format to XML.
    It handles unclosed tags, etc.
    Raises exception on parsing error.
    """
    root = html_data_as_lxml_tree(html_data)
    xml_db = _lxml_tree_to_xml_db(root)
    assert xml_db is not None, "Failed parsing the given url as xml db"
    return xml_db


def _lxml_tree_to_xml_db(root) -> Optional[XmlNodeDB]:
    tag = root.tag
    num_children = len(root)

    if not isinstance(root.tag, str):
        logging.debug(f"found invalid node with type {type(root.tag)}, skipping")
        assert num_children == 0, f"cant skip, node has {num_children} children"
        return None

    text = root.text or ""
    attributes = {}
    for key, val in root.attrib.items():
        assert isinstance(key, str)
        assert isinstance(val, str)
        attributes[key] = val

    children = []
    for child in root:
        child_xml_db = _lxml_tree_to_xml_db(child)
        if child_xml_db is not None:
            children.append(child_xml_db)

    return XmlNodeDB(
        tag=tag,
        attributes=attributes,
        text=text,
        children=children,
    )
