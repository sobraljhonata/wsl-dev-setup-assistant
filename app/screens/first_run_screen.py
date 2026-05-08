from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.ui.loading_overlay import LoadingOverlay
from app.ui.navigation_bar import NavigationBar
from app.ui.page_container import PageContainer
from app.ui.stepper import Stepper
from app.config.settings import (
    APP_STEPS,
)


class FirstRunScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref
        self.loading = None

        layout = PageContainer()

        stepper = Stepper(
            APP_STEPS=APP_STEPS,
            current_step=3,
        )

        title = Label(
            text="[b]Primeira execução da distro[/b]",
            markup=True,
            font_size=22,
            size_hint_y=0.12,
        )

        explanation = Label(
            text=(
                "Agora vamos abrir a distro Linux pela primeira vez.\n\n"
                "Nessa etapa você irá criar um usuário Linux e uma senha.\n"
                "A senha não aparece enquanto você digita. Isso é normal no Linux."
            ),
            halign="center",
            valign="middle",
            size_hint_y=0.28,
        )

        self.status_label = Label(
            text=(
                "Clique em abrir distro.\n"
                "Depois crie o usuário no terminal externo e volte para este app."
            ),
            halign="center",
            valign="middle",
            size_hint_y=0.2,
        )

        launch_button = Button(
            text="Abrir distro em terminal externo",
            size_hint_y=0.14,
        )

        launch_button.bind(on_press=lambda *_: self.launch_distro())

        self.navigation = NavigationBar(
            on_back=self.go_back,
            on_next=self.go_next,
            next_disabled=True,
        )

        layout.add_widget(stepper)
        layout.add_widget(title)
        layout.add_widget(explanation)
        layout.add_widget(self.status_label)
        layout.add_widget(launch_button)
        layout.add_widget(self.navigation)

        self.add_widget(layout)

    def launch_distro(self) -> None:
        selected_distro = self.app.selected_distro

        self._open_loading(
            f"Abrindo {selected_distro} em um terminal externo..."
        )

        self.app.async_command_service.run(
            task=lambda: self.app.wsl_service.launch_distro(selected_distro),
            on_success=self._on_launch_success,
            on_error=self._on_error,
        )

    def _on_launch_success(self, result) -> None:
        self._close_loading()

        if result.succeeded:
            self.status_label.text = (
                "A distro foi aberta em um terminal externo.\n\n"
                "1. Crie seu usuário Linux\n"
                "2. Crie sua senha\n"
                "3. Aguarde o terminal finalizar\n"
                "4. Volte para este app\n"
                "5. Clique em Próximo"
            )
            self.navigation.set_next_disabled(False)
            return

        self.status_label.text = result.stderr or "Erro ao abrir a distro."
        self.navigation.set_next_disabled(True)

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
        self.manager.current = "distro"

    def go_next(self) -> None:
        self.manager.current = "terminal"