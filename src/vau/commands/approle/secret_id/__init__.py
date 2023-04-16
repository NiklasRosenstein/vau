"""
Manage AppRole Secret IDs and Secret ID accessors.

Secret IDs are used to authenticate against an AppRole. Secret ID accessors are used to revoke Secret IDs.
"""

from typer import Context, Option


def callback(
    ctx: Context,
    role_name: str = Option(..., help="The name of the approle", metavar="ROLE_NAME"),
) -> None:
    ctx.obj = role_name
