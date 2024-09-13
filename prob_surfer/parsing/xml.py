from typing import Any, Optional
from lxml import html, etree  # type: ignore
import logging
from ..db import XmlNode, XmlNodeDB

logger = logging.getLogger(__name__)


def lxml_tree_to_xml_str(root) -> str:
    xml_content = etree.tostring(root, pretty_print=True, encoding="unicode")

    return xml_content


def _filter_lxml_tree_with_xpath(root, xpath_filter: str) -> Any:
    assert len(xpath_filter) > 0
    logger.info(f"Applying XPath query: {xpath_filter}")
    res = root.xpath(xpath_filter)

    if not isinstance(res, list):
        raise ValueError(f"Supplied XPath query is invalid: {xpath_filter}")
    elif len(res) == 0:
        raise ValueError("Supplied XPath query returned 0 results on the supplied url")
    elif len(res) == 1:
        return res[0]
    else:
        # Since an XPATh query can return >1 results, we aggregate them under a new XML root
        root = etree.Element("XPath_root")
        for child in res:
            root.append(child)
        return root


def html_data_as_lxml_tree(html_data: str) -> Any:
    try:
        root = html.fromstring(html_data)
    except Exception as e:
        raise ValueError("Failed converting html data to xml!") from e
    return root


def html_data_as_xml_db(
    html_data: str, xpath_filter: Optional[str] = None
) -> XmlNodeDB:
    """
    Converts HTML format to XML.
    It handles unclosed tags, etc.
    Raises exception on parsing error.
    """
    root = html_data_as_lxml_tree(html_data)
    if xpath_filter:
        root = _filter_lxml_tree_with_xpath(root, xpath_filter)
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
        node=XmlNode(
            tag=tag,
            attributes=attributes,
            text=text,
        ),
        children=children,
    )
