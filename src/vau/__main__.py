from typer_builder import build_app_from_module


def main() -> None:
    app = build_app_from_module(
        "vau.commands", typer_options={"no_args_is_help": True, "pretty_exceptions_enable": False}
    )
    app()


if __name__ == "__main__":
    main()
