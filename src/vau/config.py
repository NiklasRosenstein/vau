from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import databind.json


@dataclass
class VaultAlias:
    addr: str
    token: str | None
    namespace: str | None


@dataclass
class Config:
    aliases: dict[str, VaultAlias]
    default_alias: str | None

    def __post_init__(self) -> None:
        self.path: Path | None = None

    @staticmethod
    def from_file(file: Path) -> Config:
        if file.exists():
            with file.open("r") as fp:
                raw_data = json.load(fp)
            config = databind.json.load(raw_data, Config)
        else:
            config = Config(aliases={}, default_alias=None)
        config.path = file
        return config

    def to_file(self, file: Path | None = None) -> None:
        if file is None:
            if self.path is None:
                raise ValueError("no path specified")
            file = self.path
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("w") as fp:
            json.dump(databind.json.dump(self, Config), fp, indent=2)
