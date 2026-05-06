from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner


class DistroScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
        )

        title = Label(
            text="Escolha uma distribuição Linux",
            font_size=22,
            size_hint_y=0.15,
        )

        explanation = Label(
            text=(
                "Ubuntu é recomendado para iniciantes.\n"
                "Você poderá instalar ferramentas de desenvolvimento nele."
            ),
            size_hint_y=0.2,
        )

        self.status_label = Label(
            text="Clique em carregar distros",
            size_hint_y=0.1,
        )

        self.spinner = Spinner(
            text="Ubuntu",
            values=("Ubuntu",),
            size_hint_y=0.12,
        )

        load_button = Button(
            text="Carregar distros",
            size_hint_y=0.12,
        )

        install_button = Button(
            text="Instalar distro",
            size_hint_y=0.12,
        )

        next_button = Button(
            text="Ir para terminal assistido",
            size_hint_y=0.12,
        )

        load_button.bind(on_press=self.load_distros)
        install_button.bind(on_press=self.install_distro)
        next_button.bind(on_press=self.go_next)

        layout.add_widget(title)
        layout.add_widget(explanation)
        layout.add_widget(self.status_label)
        layout.add_widget(self.spinner)
        layout.add_widget(load_button)
        layout.add_widget(install_button)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def load_distros(self, *_):
        self.status_label.text = "Carregando distros..."

        self.app.async_command_service.run(
            task=self.app.wsl_service.list_available_distros_result,
            on_success=self._on_distros_loaded,
            on_error=self._on_error,
        )

    def _on_distros_loaded(self, result):
        if not result.succeeded:
            self.status_label.text = result.stderr
            return

        distros = self.app.wsl_service._parse_available_distros(
            result.stdout
        )

        if not distros:
            self.status_label.text = "Nenhuma distro encontrada"
            return

        distro_names = [distro.name for distro in distros]

        self.spinner.values = distro_names
        self.spinner.text = distro_names[0]

        self.status_label.text = (
            f"{len(distro_names)} distros encontradas"
        )

    def install_distro(self, *_):
        selected_distro = self.spinner.text

        self.status_label.text = (
            f"Instalando {selected_distro}..."
        )

        self.app.async_command_service.run(
            task=lambda: self.app.wsl_service.install_distro(
                selected_distro
            ),
            on_success=self._on_install_success,
            on_error=self._on_error,
        )

    def _on_install_success(self, result):
        if result.succeeded:
            self.status_label.text = (
                "Instalação concluída."
            )
        else:
            self.status_label.text = result.stderr

    def _on_error(self, error):
        self.status_label.text = f"Erro: {error}"

    def go_next(self, *_):
        self.app.selected_distro = self.spinner.text
        self.manager.current = "terminal"