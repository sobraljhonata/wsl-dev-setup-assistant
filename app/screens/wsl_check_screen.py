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


class WslCheckScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref
        self.loading = None

        layout = PageContainer()

        stepper = Stepper(
            APP_STEPS=APP_STEPS,
            current_step=1,
        )

        title = Label(
            text="[b]Distros Linux instaladas[/b]",
            markup=True,
            font_size=24,
            size_hint_y=0.15,
        )

        explanation = Label(
            text=(
                "O WSL permite executar Linux dentro do Windows.\n"
                "Vamos verificar quais distros estão instaladas e qual versão do WSL elas usam."
            ),
            halign="center",
            valign="middle",
            size_hint_y=0.25,
        )

        self.status_label = Label(
            text="Clique para verificar o WSL.",
            halign="center",
            valign="middle",
            size_hint_y=0.2,
        )

        check_button = Button(
            text="Verificar WSL",
            size_hint_y=0.14,
        )

        check_button.bind(on_press=lambda *_: self.check_wsl())

        self.navigation = NavigationBar(
            on_back=self.go_back,
            on_next=self.go_next,
            next_disabled=True,
        )

        layout.add_widget(stepper)
        layout.add_widget(title)
        layout.add_widget(explanation)
        layout.add_widget(self.status_label)
        layout.add_widget(check_button)
        layout.add_widget(self.navigation)

        self.add_widget(layout)

    def on_pre_enter(self, *_args) -> None:
        self.navigation.set_next_disabled(True)

    def check_wsl(self) -> None:
        self.status_label.text = "Verificando WSL..."
        self.loading = LoadingOverlay("Verificando WSL...")
        self.loading.open()

        self.app.async_command_service.run(
            task=self.app.wsl_service.get_status,
            on_success=self._on_success,
            on_error=self._on_error,
        )

    def _on_success(self, result) -> None:
        self._close_loading()

        if result.succeeded:
            self.status_label.text = result.stdout or "WSL verificado com sucesso."
            self.navigation.set_next_disabled(False)
            return

        self.status_label.text = (
            result.stderr
            or "Não foi possível verificar o WSL. Verifique se ele está instalado."
        )
        self.navigation.set_next_disabled(True)

    def _on_error(self, error: Exception) -> None:
        self._close_loading()
        self.status_label.text = f"Erro inesperado: {error}"
        self.navigation.set_next_disabled(True)

    def _close_loading(self) -> None:
        if self.loading:
            self.loading.dismiss()
            self.loading = None

    def go_back(self) -> None:
        self.manager.current = "welcome"

    def go_next(self) -> None:
        self.manager.current = "distro"