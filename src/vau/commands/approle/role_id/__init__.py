"""
Manage AppRole Role IDs.

Role IDs are used to authenticate against an AppRole. Role IDs are not secret and can be distributed freely.
"""

from typer import Context, Option


def callback(
    ctx: Context,
    role_name: str = Option(..., help="The name of the approle", metavar="ROLE_NAME"),
) -> None:
    ctx.obj = role_name
