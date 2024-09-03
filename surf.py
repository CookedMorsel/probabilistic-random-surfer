import click  # type: ignore
import logging
from prob_surfer.parsing.html import get_url_data_as_html

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler(),  # Log messages to the console
    ],
)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--url", default="https://en.wikipedia.org/wiki/Random_surfing_model")
def main(url: str):

    html_data = get_url_data_as_html(url)
    with open("out.html", "w", encoding="utf-8") as f:
        f.write(html_data)
    # logger.info(data.text)


if __name__ == "__main__":
    main()
