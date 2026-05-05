from app.domain.command_result import CommandResult
from app.services.wsl_service import WslService


class DevSetupService:
    def __init__(self, wsl_service: WslService | None = None) -> None:
        self.wsl_service = wsl_service or WslService()

    def install_cli(self, distro_name: str) -> CommandResult:
        command = (
            "python3 -m pip install --user --upgrade pip && "
            "python3 -m pip install --user dev-setup-cli-jhonata"
        )

        return self.wsl_service.run_in_distro(distro_name, command)

    def show_help(self, distro_name: str) -> CommandResult:
        return self.wsl_service.run_in_distro(distro_name, "devsetup --help")

    def run_doctor(self, distro_name: str) -> CommandResult:
        return self.wsl_service.run_in_distro(distro_name, "devsetup doctor")

    def dry_run_backend_profile(self, distro_name: str) -> CommandResult:
        return self.wsl_service.run_in_distro(
            distro_name,
            "devsetup --dry-run --yes profile backend",
        )