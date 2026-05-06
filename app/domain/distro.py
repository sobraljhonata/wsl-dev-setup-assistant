from dataclasses import dataclass


@dataclass(frozen=True)
class Distro:
    name: str
    friendly_name: str

    def __str__(self) -> str:
        return self.friendly_name