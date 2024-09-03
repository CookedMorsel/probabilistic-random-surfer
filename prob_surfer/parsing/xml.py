from lxml import html, etree  # type: ignore


def html_to_xml_db(html_data: str) -> str:
    """
    Converts HTML format to XML.
    It handles unclosed tags, etc.
    Raises exception on parsing error.
    """
    data = html.fromstring(html_data)
    xml_content = etree.tostring(data, pretty_print=True, encoding="unicode")

    return xml_content


def get_url_data_as_lxml_tree(html_data: str):
    """
    Converts HTML format to XML.
    It handles unclosed tags, etc.
    Raises exception on parsing error.
    """
    root = html.fromstring(html_data)
    return root
