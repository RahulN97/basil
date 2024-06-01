from dataclasses import dataclass


@dataclass(frozen=True)
class LinkToken:
    token: str
