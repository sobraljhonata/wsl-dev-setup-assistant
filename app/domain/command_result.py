from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    command: str
    stdout: str
    stderr: str
    return_code: int

    @property
    def succeeded(self) -> bool:
        return self.return_code == 0