from dataclasses import dataclass


@dataclass(frozen=True)
class Distro:
    name: str
    friendly_name: str