from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner

from app.config.settings import DEFAULT_DISTRO
from app.ui.loading_overlay import LoadingOverlay
from app.ui.navigation_bar import NavigationBar
from app.ui.page_container import PageContainer
from app.ui.stepper import Stepper
from app.config.settings import (
    APP_STEPS,
)


class DistroScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref
        self.loading = None

        layout = PageContainer()

        stepper = Stepper(
            APP_STEPS=APP_STEPS,
            current_step=2,
        )

        title = Label(
            text="[b]Escolha uma distribuição Linux[/b]",
            markup=True,
            font_size=22,
            size_hint_y=0.12,
        )

        explanation = Label(
            text=(
                "Ubuntu 24.04 LTS é recomendado para iniciantes.\n"
                "Depois da instalação, a primeira execução criará seu usuário Linux."
            ),
            halign="center",
            valign="middle",
            size_hint_y=0.18,
        )

        self.status_label = Label(
            text="Clique em carregar distros.",
            halign="center",
            valign="middle",
            size_hint_y=0.14,
        )

        self.spinner = Spinner(
            text=DEFAULT_DISTRO,
            values=(DEFAULT_DISTRO,),
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

        load_button.bind(on_press=lambda *_: self.load_distros())
        install_button.bind(on_press=lambda *_: self.install_distro())

        self.navigation = NavigationBar(
            on_back=self.go_back,
            on_next=self.go_next,
            next_disabled=True,
        )

        layout.add_widget(stepper)
        layout.add_widget(title)
        layout.add_widget(explanation)
        layout.add_widget(self.status_label)
        layout.add_widget(self.spinner)
        layout.add_widget(load_button)
        layout.add_widget(install_button)
        layout.add_widget(self.navigation)

        self.add_widget(layout)

    def on_pre_enter(self, *_args) -> None:
        self.navigation.set_next_disabled(True)

    def load_distros(self) -> None:
        self._open_loading("Carregando distros disponíveis...")

        self.app.async_command_service.run(
            task=self.app.wsl_service.fetch_available_distros,
            on_success=self._on_distros_loaded,
            on_error=self._on_error,
        )

    def _on_distros_loaded(self, result) -> None:
        self._close_loading()

        if not result.succeeded:
            self.status_label.text = result.stderr or "Erro ao carregar distros."
            self.navigation.set_next_disabled(True)
            return

        distros = self.app.wsl_service.parse_available_distros(result.stdout)

        if not distros:
            self.status_label.text = "Nenhuma distro encontrada."
            self.navigation.set_next_disabled(True)
            return

        distro_names = [distro.name for distro in distros]

        self.spinner.values = distro_names
        self.spinner.text = (
            DEFAULT_DISTRO if DEFAULT_DISTRO in distro_names else distro_names[0]
        )

        self.status_label.text = f"{len(distro_names)} distros encontradas."
        self.navigation.set_next_disabled(False)

    def install_distro(self) -> None:
        selected_distro = self.spinner.text
        self.app.selected_distro = selected_distro

        self._open_loading(
            f"Instalando {selected_distro}...\n"
            "Esse processo pode demorar e pode exigir reinício do Windows."
        )

        self.app.async_command_service.run(
            task=lambda: self.app.wsl_service.install_distro(selected_distro),
            on_success=self._on_install_success,
            on_error=self._on_error,
        )

    def _on_install_success(self, result) -> None:
        self._close_loading()

        if result.succeeded:
            self.status_label.text = (
                "Instalação concluída. Agora abra a primeira execução da distro."
            )
            return

        self.status_label.text = result.stderr or "Erro ao instalar distro."
        self.navigation.set_next_disabled(False)

    def _on_error(self, error: Exception) -> None:
        self._close_loading()
        self.status_label.text = f"Erro inesperado: {error}"
        self.navigation.set_next_disabled(True)

    def _open_loading(self, message: str) -> None:
        self.loading = LoadingOverlay(message)
        self.loading.open()

    def _close_loading(self) -> None:
        if self.loading:
            self.loading.dismiss()
            self.loading = None

    def go_back(self) -> None:
        self.manager.current = "wsl_check"

    def go_next(self) -> None:
        self.app.selected_distro = self.spinner.text
        self.manager.current = "first_run"