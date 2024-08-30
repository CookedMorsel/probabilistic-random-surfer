import requests  # type: ignore
import logging

logger = logging.getLogger(__name__)


def get_url_data_as_html(url: str) -> str:
    logger.debug(f"retrieving {url}")

    data = requests.get(url)
    data.raise_for_status()

    html_raw = data.text
    return html_raw
