from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView


class LoadingOverlay(ModalView):
    def __init__(self, message: str = "Carregando...", **kwargs):
        super().__init__(
            auto_dismiss=False,
            size_hint=(0.5, 0.25),
            **kwargs,
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
        )

        label = Label(
            text=message,
        )

        layout.add_widget(label)

        self.add_widget(layout)

    def update_message(self, message: str) -> None:
        if self.children:
            layout = self.children[0]

            if layout.children:
                label = layout.children[0]
                label.text = message