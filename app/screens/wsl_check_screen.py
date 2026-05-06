from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class WslCheckScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
        )

        title = Label(
            text="Verificação do WSL",
            font_size=24,
            size_hint_y=0.15,
        )

        explanation = Label(
            text=(
                "O WSL permite executar Linux dentro do Windows.\n"
                "Antes de continuar, vamos verificar se ele está disponível."
            ),
            size_hint_y=0.25,
        )

        self.status_label = Label(
            text="Clique para verificar o WSL.",
            size_hint_y=0.2,
        )

        check_button = Button(
            text="Verificar WSL",
            size_hint_y=0.15,
        )

        self.next_button = Button(
            text="Próximo",
            size_hint_y=0.15,
            disabled=True,
        )

        check_button.bind(on_press=self.check_wsl)
        self.next_button.bind(on_press=self.go_next)

        layout.add_widget(title)
        layout.add_widget(explanation)
        layout.add_widget(self.status_label)
        layout.add_widget(check_button)
        layout.add_widget(self.next_button)

        self.add_widget(layout)

    def check_wsl(self, *_):
        self.status_label.text = "Verificando WSL..."

        self.app.async_command_service.run(
            task=self.app.wsl_service.get_status,
            on_success=self._on_success,
            on_error=self._on_error,
        )

    def _on_success(self, result):
        if result.succeeded:
            self.status_label.text = result.stdout or "WSL verificado com sucesso."
            self.next_button.disabled = False
            return

        self.status_label.text = (
            result.stderr
            or "Não foi possível verificar o WSL. Verifique se ele está instalado."
        )
        self.next_button.disabled = True

    def _on_error(self, error):
        self.status_label.text = f"Erro inesperado: {error}"
        self.next_button.disabled = True

    def go_next(self, *_):
        self.manager.current = "distro"