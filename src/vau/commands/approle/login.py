import json

from hvac.api.auth_methods.approle import AppRole  # type: ignore[import]
from rich import print
from typer import Option


def main(
    client: AppRole,
    role_id: str = Option(..., help="Role ID", metavar="ROLE_ID"),
    secret_id: str = Option(..., help="Secret ID", metavar="SECRET_ID"),
) -> None:
    """
    Login to vault using an Approle and retrieve a token.

    The token and its metadata will be printed to stdout in JSON format. The JSON will look something like this:

    {
        "client_token": "hvs...",
        "accessor": "ecB...",
        "policies": ["default"],
        "token_policies": ["default"],
        "metadata": { "role_name": "test" },
        "lease_duration": 86400,
        "renewable": true,
        "entity_id": "4e939730-4cb2-e996-4c49-ff3914d9749b",
        "token_type": "service",
        "orphan": true,
        "mfa_requirement": null,
        "num_uses": 0
    }
    """

    response = client.login(role_id=role_id, secret_id=secret_id)["auth"]
    print(json.dumps(response, indent=2))
