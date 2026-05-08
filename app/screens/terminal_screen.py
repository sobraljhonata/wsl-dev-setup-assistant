from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.config.settings import APP_STEPS
from app.ui.navigation_bar import NavigationBar
from app.ui.screen_menu import ScreenMenu
from app.ui.stepper import Stepper
from app.ui.terminal_widget import TerminalWidget


class TerminalScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
        )

        stepper = Stepper(
            APP_STEPS=APP_STEPS,
            current_step=4,
        )

        menu = ScreenMenu(
            navigate_to=self.navigate_to,
        )

        title = Label(
            text="[b]Terminal assistido[/b]",
            markup=True,
            font_size=22,
            size_hint_y=0.08,
        )

        subtitle = Label(
            text=(
                "Use os botões guiados para abrir um terminal Linux real. "
                "Use o campo abaixo para comandos simples."
            ),
            size_hint_y=0.08,
        )

        devsetup_buttons = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=0.14,
        )

        self.bootstrap_button = Button(text="Preparar Python/Pip")
        self.install_cli_button = Button(text="Instalar CLI")
        self.help_button = Button(text="devsetup --help")
        self.doctor_button = Button(text="devsetup doctor")
        self.dry_run_button = Button(text="Simular backend")

        self.bootstrap_button.bind(on_press=lambda *_: self.bootstrap_python())
        self.install_cli_button.bind(on_press=lambda *_: self.install_devsetup_cli())
        self.help_button.bind(on_press=lambda *_: self.run_devsetup_help())
        self.doctor_button.bind(on_press=lambda *_: self.run_devsetup_doctor())
        self.dry_run_button.bind(on_press=lambda *_: self.run_devsetup_dry_run())

        devsetup_buttons.add_widget(self.bootstrap_button)
        devsetup_buttons.add_widget(self.install_cli_button)
        devsetup_buttons.add_widget(self.help_button)
        devsetup_buttons.add_widget(self.doctor_button)
        devsetup_buttons.add_widget(self.dry_run_button)

        basic_buttons = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=0.14,
        )

        pwd_button = Button(text="pwd")
        ls_button = Button(text="ls")
        whoami_button = Button(text="whoami")
        python_button = Button(text="python3 --version")

        pwd_button.bind(
            on_press=lambda *_: self.run_simple_command(
                "pwd",
                "Mostra o diretório atual dentro do Linux.",
            )
        )

        ls_button.bind(
            on_press=lambda *_: self.run_simple_command(
                "ls",
                "Lista arquivos e pastas do diretório atual.",
            )
        )

        whoami_button.bind(
            on_press=lambda *_: self.run_simple_command(
                "whoami",
                "Mostra o usuário Linux atual.",
            )
        )

        python_button.bind(
            on_press=lambda *_: self.run_simple_command(
                "python3 --version",
                "Mostra a versão do Python instalada na distro.",
            )
        )

        basic_buttons.add_widget(pwd_button)
        basic_buttons.add_widget(ls_button)
        basic_buttons.add_widget(whoami_button)
        basic_buttons.add_widget(python_button)

        self.terminal = TerminalWidget(
            on_execute=self.run_custom_command,
        )

        navigation = NavigationBar(
            on_home=self.go_home,
            on_back=self.go_back,
        )

        layout.add_widget(stepper)
        layout.add_widget(menu)
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(devsetup_buttons)
        layout.add_widget(basic_buttons)
        layout.add_widget(self.terminal)
        layout.add_widget(navigation)

        self.add_widget(layout)

    def on_pre_enter(self, *_args) -> None:
        if self.terminal.output.text:
            return

        self.terminal.append_output("Bem-vindo ao Terminal Assistido.")
        self.terminal.append_output("Dica: comece com 'whoami', 'pwd' e 'ls'.")
        self.terminal.append_output(
            "Para instalações e comandos com sudo, use os botões guiados."
        )

    def bootstrap_python(self) -> None:
        self._run_external(
            loading_message=(
                "Será aberto um terminal Linux real.\n\n"
                "Você aprenderá:\n"
                "- sudo\n"
                "- apt\n"
                "- instalação de pacotes\n\n"
                "Digite sua senha Linux quando solicitado."
            ),
            task=lambda: self.app.devsetup_service.bootstrap_python(
                self.app.selected_distro
            ),
        )

    def install_devsetup_cli(self) -> None:
        self._run_external(
            loading_message=(
                "Será aberto um terminal Linux real.\n\n"
                "O Dev Setup CLI será instalado usando pipx."
            ),
            task=lambda: self.app.devsetup_service.install_cli(
                self.app.selected_distro
            ),
        )

    def run_devsetup_help(self) -> None:
        self._run_external(
            loading_message="Abrindo ajuda do Dev Setup CLI em terminal real...",
            task=lambda: self.app.devsetup_service.show_help(
                self.app.selected_distro
            ),
        )

    def run_devsetup_doctor(self) -> None:
        self._run_external(
            loading_message="Executando doctor em terminal real...",
            task=lambda: self.app.devsetup_service.run_doctor(
                self.app.selected_distro
            ),
        )

    def run_devsetup_dry_run(self) -> None:
        self._run_external(
            loading_message="Simulando backend em terminal real...",
            task=lambda: self.app.devsetup_service.dry_run_backend_profile(
                self.app.selected_distro
            ),
        )

    def run_simple_command(self, command: str, explanation: str) -> None:
        self.terminal.append_output("")
        self.terminal.append_output(f"Explicação: {explanation}")
        self.terminal.append_output(f"Executando: {command}")

        self.app.async_command_service.run(
            task=lambda: self.app.wsl_service.run_in_distro(
                self.app.selected_distro,
                command,
            ),
            on_success=self._on_command_success,
            on_error=self._on_error,
        )

    def run_custom_command(self, command: str) -> None:
        self.run_simple_command(
            command,
            "Comando digitado manualmente pelo usuário.",
        )

    def _run_external(self, loading_message, task) -> None:
        self.terminal.append_output("")
        self.terminal.append_output(loading_message)

        self.app.async_command_service.run(
            task=task,
            on_success=self._on_external_success,
            on_error=self._on_error,
        )

    def _on_external_success(self, result) -> None:
        self.terminal.append_output(f"$ {result.command}")

        if result.stdout:
            self.terminal.append_output(result.stdout)

        if result.stderr:
            self.terminal.append_output(result.stderr)

    def _on_command_success(self, result) -> None:
        self.terminal.append_output(f"$ {result.command}")

        if result.stdout:
            self.terminal.append_output(result.stdout)

        if result.stderr:
            self.terminal.append_output(result.stderr)

        if not result.succeeded:
            self.terminal.append_output(
                "O comando retornou erro. Leia a mensagem acima para entender o motivo."
            )

    def _on_error(self, error: Exception) -> None:
        self.terminal.append_output(f"Erro inesperado: {error}")

    def navigate_to(self, screen_name: str) -> None:
        self.manager.current = screen_name

    def go_home(self) -> None:
        self.manager.current = "welcome"

    def go_back(self) -> None:
        self.manager.current = "first_run"