from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        title = Label(
            text="WSL Dev Setup Assistant",
            font_size=24,
        )

        subtitle = Label(
            text="Vamos configurar seu ambiente Linux no Windows",
        )

        start_button = Button(
            text="Começar",
            size_hint_y=0.2,
        )

        start_button.bind(on_press=self.go_next)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def go_next(self, *_):
        self.manager.current = "wsl_check"