import subprocess

from app.domain.command_result import CommandResult


class CommandRunner:
    def run(self, command: list[str]) -> CommandResult:
        try:
            completed_process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=False,
            )

            return CommandResult(
                command=" ".join(command),
                stdout=completed_process.stdout.strip(),
                stderr=completed_process.stderr.strip(),
                return_code=completed_process.returncode,
            )
        except FileNotFoundError as error:
            return CommandResult(
                command=" ".join(command),
                stdout="",
                stderr=(
                    f"Comando não encontrado: {command[0]}. "
                    "Se você está rodando dentro do WSL, execute este app no Windows "
                    "ou garanta que wsl.exe esteja acessível."
                ),
                return_code=127,
            )