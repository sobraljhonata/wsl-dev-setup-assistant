from app.domain.command_result import CommandResult
from app.domain.distro import Distro
from app.services.command_runner import CommandRunner

WSL_COMMAND = "wsl.exe"


class WslService:
    def __init__(self, runner: CommandRunner | None = None) -> None:
        self.runner = runner or CommandRunner()

    def get_status(self) -> CommandResult:
        return self.runner.run([WSL_COMMAND, "--status"])

    def list_available_distros(self) -> list[Distro]:
        result = self.runner.run([WSL_COMMAND, "--list", "--online"])

        if not result.succeeded:
            return []

        return self._parse_available_distros(result.stdout)

    def list_installed_distros(self) -> CommandResult:
        return self.runner.run([WSL_COMMAND, "--list", "--verbose"])

    def install_distro(self, distro_name: str) -> CommandResult:
        return self.runner.run([WSL_COMMAND, "--install", "-d", distro_name])

    def launch_distro(self, distro_name: str) -> CommandResult:
        return self.runner.run([WSL_COMMAND, "-d", distro_name])

    def run_in_distro(self, distro_name: str, command: str) -> CommandResult:
        return self.runner.run(
            [
                WSL_COMMAND,
                "-d",
                distro_name,
                "--",
                "bash",
                "-lc",
                command,
            ]
        )

    def _parse_available_distros(self, output: str) -> list[Distro]:
        distros: list[Distro] = []

        for line in output.splitlines():
            cleaned_line = line.strip()

            if not cleaned_line:
                continue

            if cleaned_line.lower().startswith("name"):
                continue

            if cleaned_line.startswith("-"):
                continue

            parts = cleaned_line.split(maxsplit=1)
            name = parts[0]
            friendly_name = parts[1] if len(parts) > 1 else name

            if name.lower() in {"following", "install"}:
                continue

            distros.append(Distro(name=name, friendly_name=friendly_name))

        return distros

    def list_available_distros_result(self) -> CommandResult:
        return self.runner.run([WSL_COMMAND, "--list", "--online"])