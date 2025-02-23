from importlib import resources
from pathlib import Path

import click


@click.group()
def main():
    pass


@main.command()
def ping():
    """Debug."""
    click.echo("pong, from byssal")


@main.command()
def init():
    """Initialize a new Byssal project."""
    project_path = Path.cwd()

    data_path = project_path / "data"
    data_path.mkdir()
    click.echo(f"Created data subdirectory: {data_path}")

    try:
        with resources.open_text(
            "byssal.templates",
            "settings.py",
        ) as template_file:
            settings_content = template_file.read()
    except Exception as e:
        click.echo(f"Failed to load settings template: {e}")
        return

    settings_file = project_path / "settings.py"
    settings_file.write_text(settings_content)
    click.echo(f"Created settings file: {settings_file}")


if __name__ == "__main__":
    main()
