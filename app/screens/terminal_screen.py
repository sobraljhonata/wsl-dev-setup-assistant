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

        devsetup_buttons = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=0.16,
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
        layout.add_widget(devsetup_buttons)
        layout.add_widget(basic_buttons)
        layout.add_widget(self.terminal)

        self.add_widget(layout)

    def on_pre_enter(self, *_args) -> None:
        if self.terminal.output.text:
            return

        self.terminal.append_output("Bem-vindo ao Terminal Assistido.")
        self.terminal.append_output("Dica: comece com 'whoami', 'pwd' e 'ls'.")
        self.terminal.append_output(
            "Depois prepare Python/Pip, instale o Dev Setup CLI "
            "e rode 'devsetup --help'."
        )

    def bootstrap_python(self) -> None:
        self._run_async(
            loading_message=(
                "Preparando Python, pip e venv na distro Linux...\n"
                "Este comando pode pedir a senha do usuário Linux por usar sudo.\n"
                "Se a senha não aparecer enquanto você digita, isso é normal no Linux."
            ),
            task=lambda: self.app.devsetup_service.bootstrap_python(
                self.app.selected_distro
            ),
        )

    def install_devsetup_cli(self) -> None:
        self._run_async(
            loading_message=(
                "Instalando Dev Setup CLI dentro da distro Linux...\n"
                "Esse processo pode demorar alguns minutos."
            ),
            task=lambda: self.app.devsetup_service.install_cli(
                self.app.selected_distro
            ),
        )

    def run_devsetup_help(self) -> None:
        self._run_async(
            loading_message=(
                "Explicação: mostra todos os comandos disponíveis "
                "no Dev Setup CLI."
            ),
            task=lambda: self.app.devsetup_service.show_help(
                self.app.selected_distro
            ),
        )

    def run_devsetup_doctor(self) -> None:
        self._run_async(
            loading_message=(
                "Explicação: verifica ferramentas, versões mínimas "
                "e serviços do ambiente."
            ),
            task=lambda: self.app.devsetup_service.run_doctor(
                self.app.selected_distro
            ),
        )

    def run_devsetup_dry_run(self) -> None:
        self._run_async(
            loading_message=(
                "Explicação: simula o profile backend sem instalar nada de verdade."
            ),
            task=lambda: self.app.devsetup_service.dry_run_backend_profile(
                self.app.selected_distro
            ),
        )

    def run_guided_command(self, command: str, explanation: str) -> None:
        self._run_async(
            loading_message=(
                f"Explicação: {explanation}\n"
                f"Comando sugerido: {command}"
            ),
            task=lambda: self.app.wsl_service.run_in_distro(
                self.app.selected_distro,
                command,
            ),
        )

    def run_custom_command(self, command: str) -> None:
        self._run_async(
            loading_message=f"Executando comando digitado: {command}",
            task=lambda: self.app.wsl_service.run_in_distro(
                self.app.selected_distro,
                command,
            ),
        )

    def _run_async(self, loading_message, task) -> None:
        self.terminal.append_output("")
        self.terminal.append_output(loading_message)
        self._set_buttons_disabled(True)

        self.app.async_command_service.run(
            task=task,
            on_success=self._on_command_success,
            on_error=self._on_error,
        )

    def _on_command_success(self, result) -> None:
        self._set_buttons_disabled(False)
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
        self._set_buttons_disabled(False)
        self.terminal.append_output(f"Erro inesperado: {error}")

    def _set_buttons_disabled(self, disabled: bool) -> None:
        self.bootstrap_button.disabled = disabled
        self.install_cli_button.disabled = disabled
        self.help_button.disabled = disabled
        self.doctor_button.disabled = disabled
        self.dry_run_button.disabled = disabled