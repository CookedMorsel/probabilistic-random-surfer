import click  # type: ignore
import logging
from prob_surfer import tree_utils
from prob_surfer.parsing.html import get_url_data_as_html
from prob_surfer.parsing.xml import html_data_as_lxml_tree, lxml_tree_to_xml_db

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
@click.option("--only-print-xml", is_flag=True)
@click.option("--save-html", is_flag=True)
@click.option("--save-xml", is_flag=True)
def main(url: str, only_print_xml: bool, save_html: bool, save_xml: bool):
    html_data = get_url_data_as_html(url)

    if save_html:
        with open("out.html", "w", encoding="utf-8") as f:
            logger.info("saving html to out.html")
            f.write(html_data)

    root = html_data_as_lxml_tree(html_data)

    if save_xml:
        xml_data = lxml_tree_to_xml_db(root)
        with open("out.xml", "w", encoding="utf-8") as f:
            logger.info("saving xml to out.xml")
            f.write(xml_data)

    if only_print_xml:
        logger.info("Printing parsed xml structure and exiting")
        tree_utils.print_tree(root)


if __name__ == "__main__":
    main()
