from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class WslCheckScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.status_label = Label(text="Clique para verificar o WSL")

        check_button = Button(text="Verificar WSL")
        next_button = Button(text="Próximo")

        check_button.bind(on_press=self.check_wsl)
        next_button.bind(on_press=self.go_next)

        layout.add_widget(self.status_label)
        layout.add_widget(check_button)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def check_wsl(self, *_):
        self.status_label.text = "Verificando..."

        self.app.async_command_service.run(
            task=self.app.wsl_service.get_status,
            on_success=self._on_success,
            on_error=self._on_error,
        )

    def _on_success(self, result):
        self.status_label.text = result.stdout or "WSL verificado"

    def _on_error(self, error):
        self.status_label.text = f"Erro: {error}"

    def go_next(self, *_):
        self.manager.current = "distro"