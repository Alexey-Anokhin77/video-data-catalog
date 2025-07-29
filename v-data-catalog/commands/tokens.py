from typing import Annotated

import typer
from api.api_v1.auth.services import redis_tokens as tokens
from rich import print
from rich.markdown import Markdown

app = typer.Typer(
    name="token",
    help="Tokens management",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
) -> None:
    """
    Check if the passed token is valid - exists  or not.
    """
    print(
        f"Token [bold]{token}[/bold], [green]exists[/green]."
        if tokens.token_exist(token)
        else f"Token [bold]{token}[/bold] [bold red]does not exists[/bold red]."
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    List all tokens.
    """
    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join([""] + tokens.get_tokens())))
    print()


@app.command()
def create() -> None:
    """
    Create and save new token to bd.
    """
    new_token = tokens.generate_and_save_token()
    print(f"New token [bold]{new_token}[/bold] save to db.")


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="The Token to add."),
    ],
) -> None:
    """
    Add to provide to db.
    """
    tokens.add_token(token)
    print(f"Token [bold]{token}[/bold] add to db.")


@app.command(name="rm")
def delete(
    token: Annotated[
        str,
        typer.Argument(help="The token to delete."),
    ],
) -> None:
    """
    Delete the tokens from db.
    """
    if not tokens.token_exist(token):
        print(f"Token [bold]{token}[red] does not to exists.[/red][/bold]")
        return

    tokens.delete_token(token)
    print(f"Token [bold]{token}[/bold] remove from db.")
