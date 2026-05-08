from app.config.settings import DEVSETUP_COMMAND, DEVSETUP_PACKAGE
from app.domain.command_result import CommandResult
from app.services.wsl_service import WslService


class DevSetupService:
    def __init__(self, wsl_service: WslService | None = None) -> None:
        self.wsl_service = wsl_service or WslService()

    def bootstrap_python(self, distro_name: str) -> CommandResult:
        script = """
        echo "Preparando Python, pip, venv e pipx..."
        echo
        echo "Este comando usa sudo porque instala pacotes no sistema Linux."
        echo "Digite sua senha Linux quando solicitado."
        echo

        sudo apt update
        sudo apt install -y software-properties-common
        sudo add-apt-repository -y universe
        sudo apt update
        sudo apt install -y python3-pip python3-venv python3-full pipx

        echo
        echo "Preparação concluída."
        echo
        read -p "Pressione ENTER para continuar..."
        """

        return self.wsl_service.run_script_in_external_terminal(distro_name, script)

    def install_cli(self, distro_name: str) -> CommandResult:
        script = f"""
        echo "Instalando Dev Setup CLI com pipx..."
        echo

        pipx ensurepath
        pipx install {DEVSETUP_PACKAGE}

        echo
        echo "Instalação concluída."
        echo "Se o comando devsetup ainda não funcionar, feche e abra o terminal."
        echo
        read -p "Pressione ENTER para continuar..."
        """

        return self.wsl_service.run_script_in_external_terminal(distro_name, script)

    def show_help(self, distro_name: str) -> CommandResult:
        return self._run_devsetup_in_external_terminal(
            distro_name,
            f"{DEVSETUP_COMMAND} --help",
            "Exibindo ajuda do Dev Setup CLI",
        )

    def run_doctor(self, distro_name: str) -> CommandResult:
        return self._run_devsetup_in_external_terminal(
            distro_name,
            f"{DEVSETUP_COMMAND} doctor",
            "Executando diagnóstico do ambiente",
        )

    def dry_run_backend_profile(self, distro_name: str) -> CommandResult:
        return self._run_devsetup_in_external_terminal(
            distro_name,
            f"{DEVSETUP_COMMAND} --dry-run --yes profile backend",
            "Simulando profile backend",
        )

    def _run_devsetup_in_external_terminal(
        self,
        distro_name: str,
        command: str,
        title: str,
    ) -> CommandResult:
        script = f"""
        export PATH="$HOME/.local/bin:$PATH"

        echo "{title}"
        echo
        echo "Comando:"
        echo "{command}"
        echo

        {command}

        echo
        read -p "Pressione ENTER para continuar..."
        """

        return self.wsl_service.run_script_in_external_terminal(distro_name, script)