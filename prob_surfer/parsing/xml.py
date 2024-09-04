from lxml import html, etree  # type: ignore


def lxml_tree_to_xml_db(root) -> str:
    xml_content = etree.tostring(root, pretty_print=True, encoding="unicode")

    return xml_content


def html_data_as_lxml_tree(html_data: str):
    """
    Converts HTML format to XML.
    It handles unclosed tags, etc.
    Raises exception on parsing error.
    """
    root = html.fromstring(html_data)
    return root
