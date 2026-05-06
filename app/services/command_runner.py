import locale
import subprocess
import sys

from app.domain.command_result import CommandResult


def _get_system_encoding() -> str:
    if sys.platform.startswith("win"):
        return "mbcs"

    return locale.getpreferredencoding(False) or "utf-8"

def _decode_output(output: bytes) -> str:
    if not output:
        return ""

    if b"\x00" in output:
        return output.decode("utf-16le", errors="replace").strip()

    if sys.platform.startswith("win"):
        return output.decode("mbcs", errors="replace").strip()

    encoding = locale.getpreferredencoding(False) or "utf-8"
    return output.decode(encoding, errors="replace").strip()


class CommandRunner:
    def run(
        self,
        command: list[str],
        cwd: str | None = None,
        timeout: int = 300,
        env: dict[str, str] | None = None,
    ) -> CommandResult:
        try:
            completed_process = subprocess.run(
                command,
                capture_output=True,
                shell=False,
                cwd=cwd,
                timeout=timeout,
                env=env,
            )

            return CommandResult(
                command=" ".join(command),
                stdout=_decode_output(completed_process.stdout),
                stderr=_decode_output(completed_process.stderr),
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

        except subprocess.TimeoutExpired:
            return CommandResult(
                command=" ".join(command),
                stdout="",
                stderr="O comando excedeu o tempo limite de execução.",
                return_code=124,
            )

    def start_detached(self, command: list[str]) -> CommandResult:
        try:
            subprocess.Popen(
                command,
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )

            return CommandResult(
                command=" ".join(command),
                stdout="Processo iniciado em uma nova janela/terminal.",
                stderr="",
                return_code=0,
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