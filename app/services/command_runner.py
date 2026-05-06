import locale
import subprocess
import sys

from app.domain.command_result import CommandResult


def get_system_encoding() -> str:
    if sys.platform.startswith("win"):
        return "mbcs"

    return locale.getpreferredencoding(False) or "utf-8"


class CommandRunner:
    def run(self, command: list[str]) -> CommandResult:
        try:
            completed_process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding=get_system_encoding(),
                errors="replace",
                shell=False,
            )

            return CommandResult(
                command=" ".join(command),
                stdout=completed_process.stdout.strip(),
                stderr=completed_process.stderr.strip(),
                return_code=completed_process.returncode,
            )
        except FileNotFoundError:
            return CommandResult(
                command=" ".join(command),
                stdout="",
                stderr=(
                    f"Comando não encontrado: {command[0]}. "
                    "Execute este app no Windows com o WSL disponível."
                ),
                return_code=127,
            )