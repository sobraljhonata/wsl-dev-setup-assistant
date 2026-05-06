from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

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

        title = Label(
            text="Terminal assistido",
            font_size=22,
            size_hint_y=0.08,
        )

        subtitle = Label(
            text=(
                "Execute comandos no Linux com ajuda contextual. "
                "Use os botões sugeridos para aprender o fluxo."
            ),
            size_hint_y=0.08,
        )

        guided_buttons = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=0.16,
        )

        help_button = Button(text="devsetup --help")
        doctor_button = Button(text="devsetup doctor")
        dry_run_button = Button(text="Simular backend")
        install_cli_button = Button(text="Instalar CLI")

        help_button.bind(
            on_press=lambda *_: self.run_guided_command(
                "devsetup --help",
                "Mostra todos os comandos disponíveis no Dev Setup CLI.",
            )
        )

        doctor_button.bind(
            on_press=lambda *_: self.run_guided_command(
                "devsetup doctor",
                "Verifica se ferramentas e versões mínimas estão corretas.",
            )
        )

        dry_run_button.bind(
            on_press=lambda *_: self.run_guided_command(
                "devsetup --dry-run --yes profile backend",
                "Simula o profile backend sem instalar nada de verdade.",
            )
        )

        install_cli_button.bind(
            on_press=lambda *_: self.install_devsetup_cli()
        )

        guided_buttons.add_widget(install_cli_button)
        guided_buttons.add_widget(help_button)
        guided_buttons.add_widget(doctor_button)
        guided_buttons.add_widget(dry_run_button)

        basic_buttons = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=0.16,
        )

        pwd_button = Button(text="pwd")
        ls_button = Button(text="ls")
        whoami_button = Button(text="whoami")
        python_button = Button(text="python3 --version")

        pwd_button.bind(
            on_press=lambda *_: self.run_guided_command(
                "pwd",
                "Mostra o diretório atual dentro do Linux.",
            )
        )

        ls_button.bind(
            on_press=lambda *_: self.run_guided_command(
                "ls",
                "Lista arquivos e pastas do diretório atual.",
            )
        )

        whoami_button.bind(
            on_press=lambda *_: self.run_guided_command(
                "whoami",
                "Mostra o usuário Linux atual.",
            )
        )

        python_button.bind(
            on_press=lambda *_: self.run_guided_command(
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

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(guided_buttons)
        layout.add_widget(basic_buttons)
        layout.add_widget(self.terminal)

        self.add_widget(layout)

    def on_pre_enter(self, *_args) -> None:
        self.terminal.append_output("Bem-vindo ao Terminal Assistido.")
        self.terminal.append_output(
            "Dica: comece com 'whoami', 'pwd' e 'ls'."
        )
        self.terminal.append_output(
            "Depois instale o Dev Setup CLI e rode 'devsetup --help'."
        )

    def install_devsetup_cli(self) -> None:
        self.terminal.append_output(
            "Instalando Dev Setup CLI dentro da distro Linux..."
        )
        self.terminal.append_output(
            "Esse processo pode demorar alguns minutos."
        )

        self.app.async_command_service.run(
            task=lambda: self.app.devsetup_service.install_cli(
                self.app.selected_distro
            ),
            on_success=self._on_command_success,
            on_error=self._on_error,
        )

    def run_guided_command(self, command: str, explanation: str) -> None:
        self.terminal.append_output("")
        self.terminal.append_output(f"Explicação: {explanation}")
        self.terminal.append_output(f"Comando sugerido: {command}")

        self.app.async_command_service.run(
            task=lambda: self.app.wsl_service.run_in_distro(
                self.app.selected_distro,
                command,
            ),
            on_success=self._on_command_success,
            on_error=self._on_error,
        )

    def run_custom_command(self, command: str) -> None:
        self.terminal.append_output("")
        self.terminal.append_output(f"Executando comando digitado: {command}")

        self.app.async_command_service.run(
            task=lambda: self.app.wsl_service.run_in_distro(
                self.app.selected_distro,
                command,
            ),
            on_success=self._on_command_success,
            on_error=self._on_error,
        )

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