from collections.abc import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class NavigationBar(BoxLayout):
    def __init__(
        self,
        on_back: Callable[[], None] | None = None,
        on_next: Callable[[], None] | None = None,
        next_disabled: bool = False,
        **kwargs,
    ):
        super().__init__(
            orientation="horizontal",
            spacing=10,
            size_hint_y=0.12,
            **kwargs,
        )

        self.back_button = Button(
            text="Voltar",
            disabled=on_back is None,
        )

        self.next_button = Button(
            text="Próximo",
            disabled=next_disabled or on_next is None,
        )

        if on_back:
            self.back_button.bind(on_press=lambda *_: on_back())

        if on_next:
            self.next_button.bind(on_press=lambda *_: on_next())

        self.add_widget(self.back_button)
        self.add_widget(self.next_button)

    def set_next_disabled(self, disabled: bool) -> None:
        self.next_button.disabled = disabled