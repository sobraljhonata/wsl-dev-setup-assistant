from collections.abc import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ScreenMenu(BoxLayout):
    def __init__(
        self,
        navigate_to: Callable[[str], None],
        **kwargs,
    ):
        super().__init__(
            orientation="horizontal",
            spacing=8,
            size_hint_y=0.1,
            **kwargs,
        )

        self.navigate_to = navigate_to

        screens = [
            ("Home", "welcome"),
            ("WSL", "wsl_check"),
            ("Distro", "distro"),
            ("Primeira execução", "first_run"),
            ("Terminal", "terminal"),
        ]

        for label, screen_name in screens:
            button = Button(text=label)
            button.bind(
                on_press=lambda *_args, target=screen_name: self.navigate_to(target)
            )
            self.add_widget(button)