import click  # type: ignore
import logging
from prob_surfer import tree_utils
from prob_surfer.parsing.html import get_url_data_as_html
from prob_surfer.parsing.xml import (
    html_data_as_lxml_tree,
    lxml_tree_to_xml_str,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler(),  # Log messages to the console
    ],
)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--url", default="https://en.wikipedia.org/wiki/Random_surfing_model")
@click.option("--only-print", is_flag=True)
@click.option("--save-html", is_flag=True)
@click.option("--save-xml", is_flag=True)
def main(url: str, only_print: bool, save_html: bool, save_xml: bool):

    if save_html:
        html_data = get_url_data_as_html(url)
        with open("out.html", "w", encoding="utf-8") as f:
            logger.info("saving html to out.html")
            f.write(html_data)

    if save_xml:
        html_data = get_url_data_as_html(url)
        root = html_data_as_lxml_tree(html_data)
        xml_data = lxml_tree_to_xml_str(root)
        with open("out.xml", "w", encoding="utf-8") as f:
            logger.info("saving xml to out.xml")
            f.write(xml_data)

    db = tree_utils.get_url_as_xml_db(url)

    if only_print:
        logger.info("Printing parsed xml structure and exiting")
        tree_utils.print_tree(db)
        return

    # get_out_links_probabilities(root)


if __name__ == "__main__":
    main()
