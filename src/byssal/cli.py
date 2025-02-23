import logging
import shutil
from importlib.resources import as_file, files
from pathlib import Path

import click

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    pass


@main.command()
def ping() -> None:
    """Debug."""
    click.echo("pong, from byssal")


@main.command()
def init() -> None:
    """Initialize a new Byssal project."""
    project_path = Path.cwd()

    template_dir = files("byssal.templates") / "new_project"
    with as_file(template_dir) as src:
        shutil.copytree(src, project_path, dirs_exist_ok=True)
    logger.info(f"Copied project template from '{src}' to '{project_path}'")


if __name__ == "__main__":
    main()
