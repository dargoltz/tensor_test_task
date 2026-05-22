import typer

from .cli import app as cli_app_commands

app = typer.Typer()

app.add_typer(cli_app_commands)

if __name__ == "__main__":
    app()
