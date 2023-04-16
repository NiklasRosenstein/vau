from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from typer import Context, Option

from .._format import SecretIdAccessorListFormat


def main(
    client: AppRole,
    ctx: Context,
    format: SecretIdAccessorListFormat = Option(
        SecretIdAccessorListFormat.table, "-o", "--format", help="Output format"
    ),
) -> None:
    """List the secret id accessors for a vault approle."""

    role_name = ctx.ensure_object(str)
    accessors = [
        {"accessor_id": accessor_id, **client.read_secret_id_accessor(role_name, accessor_id)["data"]}
        for accessor_id in client.list_secret_id_accessors(role_name)["data"]["keys"]
    ]
    print(format.formatter.format_secretidaccessors(accessors))
