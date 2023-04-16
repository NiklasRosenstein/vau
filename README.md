# vau

Vau (pronounced "vow") is a simple, alternative CLI for HashiCorp Vault. Instead of providing a generic CLI, Vau
provides a CLI that is tailored to specific Vault managemend workflows. This allows for a more intuitive and
simpler CLI experience. Vau is not meant to replace the official Vault CLI, but rather to provide a more intuitive
experience for specific workflows.

## Installation

It is recommended to install Vau using Pipx:

    $ pipx install vau

## Usage

### Configuring credentials to connect to a Vault instance

Vau uses the same environment variables as the official Vault CLI. The following environment variables are supported:

* `VAULT_ADDR` - The address of the Vault instance
* `VAULT_TOKEN` - The token to use when authenticating to the Vault instance
* `VAULT_NAMESPACE` - The namespace to use when authenticating to the Vault instance

Alternatively, you can use the `--vault-addr` and `--token` flags to specify the Vault address and token. If you want
to permanently set the Vault address and token, you can use the `vau alias set` command.

    $ vau alias set --name=myvault --vault-addr=https://vault.example.com --token=s.1234567890abcdef

### Manage AppRoles using Vau

You can easily create, update, view and delete AppRoles using Vau. For example, to create an AppRole with the name `myrole`:

    $ vau approle put --role-name=myrole --policies=policy1,policy2 --secret-id-ttl=1h --token-ttl=1h

To view the details of an AppRole:

    $ vau approle get --role-name=myrole

To delete an AppRole:

    $ vau approle delete --role-name=myrole

To list all AppRoles:

    $ vau approle ls

To generate a new SecretID for an AppRole:

    $ vau approle secret-id --role-name=myrole put

To list all SecretIDs for an AppRole:

    $ vau approle secret-id --role-name=myrole ls
