import tempfile
from pathlib import Path

from app.config.settings import WINDOWS_WSL_COMMAND
from app.domain.command_result import CommandResult
from app.domain.distro import Distro
from app.services.command_runner import CommandRunner
import textwrap

WINDOWS_TERMINAL_COMMAND = "wt.exe"


class WslService:
    def __init__(self, runner: CommandRunner | None = None) -> None:
        self.runner = runner or CommandRunner()

    def get_status(self) -> CommandResult:
        return self.runner.run([WINDOWS_WSL_COMMAND, "--list", "--verbose"])

    def fetch_available_distros(self) -> CommandResult:
        return self.runner.run([WINDOWS_WSL_COMMAND, "--list", "--online"])

    def list_installed_distros(self) -> CommandResult:
        return self.runner.run([WINDOWS_WSL_COMMAND, "--list", "--verbose"])

    def install_distro(self, distro_name: str) -> CommandResult:
        return self.runner.run([WINDOWS_WSL_COMMAND, "--install", "-d", distro_name])

    def launch_distro(self, distro_name: str) -> CommandResult:
        return self.runner.start_external_terminal(
            [
                WINDOWS_TERMINAL_COMMAND,
                "new-tab",
                "--title",
                distro_name,
                WINDOWS_WSL_COMMAND,
                "-d",
                distro_name,
                "--cd",
                "~",
            ]
        )

    def run_in_distro(self, distro_name: str, command: str) -> CommandResult:
        return self.runner.run(
            [
                WINDOWS_WSL_COMMAND,
                "-d",
                distro_name,
                "--",
                "bash",
                "-lc",
                command,
            ]
        )

    def run_script_in_external_terminal(
        self,
        distro_name: str,
        script_content: str,
    ) -> CommandResult:
        script_path = self._create_temp_script(script_content)
        wsl_script_path = self._to_wsl_path(script_path)

        return self.runner.start_external_terminal(
            [
                WINDOWS_TERMINAL_COMMAND,
                "new-tab",
                "--title",
                f"{distro_name} setup",
                WINDOWS_WSL_COMMAND,
                "-d",
                distro_name,
                "--cd",
                "~",
                "--",
                "bash",
                wsl_script_path,
            ]
        )

    def parse_available_distros(self, output: str) -> list[Distro]:
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

    def _create_temp_script(self, script_content: str) -> Path:
        script_dir = Path(tempfile.gettempdir()) / "wsl-dev-setup-assistant"
        script_dir.mkdir(parents=True, exist_ok=True)

        script_path = script_dir / "setup.sh"

        normalized_script = textwrap.dedent(script_content).strip() + "\n"

        script_path.write_text(
            normalized_script,
            encoding="utf-8",
            newline="\n",
        )

        return script_path

    def _to_wsl_path(self, path: Path) -> str:
        resolved_path = path.resolve()
        drive = resolved_path.drive.replace(":", "").lower()
        relative_path = str(resolved_path)[3:].replace("\\", "/")

        return f"/mnt/{drive}/{relative_path}"