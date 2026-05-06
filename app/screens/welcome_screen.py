from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12,
        )

        title = Label(
            text="[b]WSL Dev Setup Assistant[/b]",
            markup=True,
            font_size=28,
            size_hint_y=0.2,
        )

        subtitle = Label(
            text=(
                "Este assistente vai ajudar você a:\n\n"
                "• instalar Linux no WSL\n"
                "• aprender comandos básicos do terminal\n"
                "• preparar um ambiente de desenvolvimento\n"
                "• usar o Dev Setup CLI"
            ),
            halign="center",
            valign="middle",
            size_hint_y=0.4,
        )

        explanation = Label(
            text=(
                "O objetivo não é esconder o Linux,\n"
                "mas ajudar você a aprender Linux com segurança."
            ),
            italic=True,
            size_hint_y=0.2,
        )

        start_button = Button(
            text="Começar",
            size_hint=(0.4, 0.2),
            pos_hint={"center_x": 0.5},
        )

        start_button.bind(on_press=self.go_next)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(explanation)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def go_next(self, *_):
        self.manager.current = "wsl_check"