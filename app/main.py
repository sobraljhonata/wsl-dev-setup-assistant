from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from app.services.devsetup_service import DevSetupService
from app.services.wsl_service import WslService
from app.ui.terminal_widget import TerminalWidget
from app.services.async_command_service import AsyncCommandService


class DevSetupLauncherApp(App):
    def build(self) -> BoxLayout:
        self.wsl_service = WslService()
        self.devsetup_service = DevSetupService(self.wsl_service)
        self.async_command_service = AsyncCommandService()
        self.selected_distro = "Ubuntu"

        root = BoxLayout(orientation="vertical", padding=12, spacing=8)

        title = Label(
            text="Dev Setup Launcher",
            size_hint_y=0.08,
            bold=True,
        )

        subtitle = Label(
            text="Assistente educacional para WSL, Linux e Dev Setup CLI",
            size_hint_y=0.06,
        )

        self.distro_spinner = Spinner(
            text="Ubuntu",
            values=("Ubuntu",),
            size_hint_y=0.08,
        )
        self.distro_spinner.bind(text=self._on_distro_selected)

        buttons = BoxLayout(size_hint_y=0.16, spacing=8)

        check_wsl_button = Button(text="Verificar WSL")
        list_distros_button = Button(text="Listar distros")
        install_distro_button = Button(text="Instalar distro")
        launch_distro_button = Button(text="Primeira execução")

        check_wsl_button.bind(on_press=lambda *_: self.check_wsl())
        list_distros_button.bind(on_press=lambda *_: self.list_distros())
        install_distro_button.bind(on_press=lambda *_: self.install_distro())
        launch_distro_button.bind(on_press=lambda *_: self.launch_distro())

        buttons.add_widget(check_wsl_button)
        buttons.add_widget(list_distros_button)
        buttons.add_widget(install_distro_button)
        buttons.add_widget(launch_distro_button)

        guided_buttons = BoxLayout(size_hint_y=0.16, spacing=8)

        install_cli_button = Button(text="Instalar Dev Setup CLI")
        help_button = Button(text="Ver help")
        doctor_button = Button(text="Rodar doctor")
        dry_run_button = Button(text="Simular backend")

        install_cli_button.bind(on_press=lambda *_: self.install_devsetup())
        help_button.bind(on_press=lambda *_: self.show_devsetup_help())
        doctor_button.bind(on_press=lambda *_: self.run_doctor())
        dry_run_button.bind(on_press=lambda *_: self.dry_run_backend())

        guided_buttons.add_widget(install_cli_button)
        guided_buttons.add_widget(help_button)
        guided_buttons.add_widget(doctor_button)
        guided_buttons.add_widget(dry_run_button)

        self.terminal = TerminalWidget(on_execute=self.run_custom_command)

        root.add_widget(title)
        root.add_widget(subtitle)
        root.add_widget(self.distro_spinner)
        root.add_widget(buttons)
        root.add_widget(guided_buttons)
        root.add_widget(self.terminal)

        self.terminal.append_output(
            "Bem-vindo! Comece verificando se o WSL está instalado."
        )
        self.terminal.append_output(
            "Dica: a primeira execução da distro abrirá um terminal oficial."
        )
        self.terminal.append_output(
            "Ao criar a senha Linux, ela não aparece na tela. Isso é normal."
        )

        return root

    def _on_distro_selected(self, _spinner: Spinner, text: str) -> None:
        self.selected_distro = text
        self.terminal.append_output(f"Distro selecionada: {text}")

    def check_wsl(self) -> None:
        self.run_async_command(
            "Verificando WSL...",
            self.wsl_service.get_status,
        )

    def list_distros(self) -> None:
        self.terminal.append_output("Listando distros disponíveis...")

        self.async_command_service.run(
            task=self.wsl_service.list_available_distros_result,
            on_success=self._handle_distros_result,
            on_error=lambda error: self.terminal.append_output(
                f"Erro inesperado: {error}"
            ),
        )

    def install_distro(self) -> None:
        self.run_async_command(
            (
                f"Instalando distro {self.selected_distro}. "
                "Pode ser necessário reiniciar o Windows."
            ),
            lambda: self.wsl_service.install_distro(self.selected_distro),
        )

    def launch_distro(self) -> None:
        self.terminal.append_output(
            "Abrindo a primeira execução da distro."
        )
        self.terminal.append_output(
            "Crie um usuário Linux comum e uma senha."
        )
        self.terminal.append_output(
            "A senha não aparecerá enquanto você digita. Isso é esperado."
        )

        result = self.wsl_service.launch_distro(self.selected_distro)
        self._print_result(result.command, result.stdout, result.stderr)

    def install_devsetup(self) -> None:
        self.run_async_command(
            "Instalando Dev Setup CLI...",
            lambda: self.devsetup_service.install_cli(self.selected_distro),
        )


    def show_devsetup_help(self) -> None:
        self.run_async_command(
            "Carregando help do Dev Setup CLI...",
            lambda: self.devsetup_service.show_help(self.selected_distro),
        )


    def run_doctor(self) -> None:
        self.run_async_command(
            "Executando devsetup doctor...",
            lambda: self.devsetup_service.run_doctor(self.selected_distro),
        )


    def dry_run_backend(self) -> None:
        self.run_async_command(
            "Simulando profile backend...",
            lambda: self.devsetup_service.dry_run_backend_profile(self.selected_distro),
        )


    def run_custom_command(self, command: str) -> None:
        self.run_async_command(
            f"Executando comando: {command}",
            lambda: self.wsl_service.run_in_distro(self.selected_distro, command),
        )

    def _print_result(self, command: str, stdout: str, stderr: str) -> None:
        self.terminal.append_output(f"$ {command}")

        if stdout:
            self.terminal.append_output(stdout)

        if stderr:
            self.terminal.append_output(stderr)

    def run_async_command(
        self,
        loading_message: str,
        task,
    ) -> None:
        self.terminal.append_output(loading_message)

        self.async_command_service.run(
            task=task,
            on_success=lambda result: self._print_result(
                result.command,
                result.stdout,
                result.stderr,
            ),
            on_error=lambda error: self.terminal.append_output(
                f"Erro inesperado: {error}"
            ),
        )

    def _handle_distros_result(self, result) -> None:
        self._print_result(result.command, result.stdout, result.stderr)

        if not result.succeeded:
            self.terminal.append_output(
                "Não foi possível listar distros. "
                "Verifique se o app está rodando no Windows com WSL disponível."
            )
            return

        distros = self.wsl_service._parse_available_distros(result.stdout)

        if not distros:
            self.terminal.append_output("Nenhuma distro encontrada.")
            return

        self.distro_spinner.values = tuple(distro.name for distro in distros)

        self.terminal.append_output("Distros disponíveis:")

        for distro in distros:
            self.terminal.append_output(f"- {distro.name}: {distro.friendly_name}")


if __name__ == "__main__":
    DevSetupLauncherApp().run()