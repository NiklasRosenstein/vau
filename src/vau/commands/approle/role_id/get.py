from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from typer import Context


def main(client: AppRole, ctx: Context) -> None:
    role_name = ctx.ensure_object(str)
    role_id = client.read_role_id(role_name)["data"]["role_id"]
    print(role_id)
