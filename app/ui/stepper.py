from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class Stepper(BoxLayout):
    def __init__(
        self,
        APP_STEPS: list[str],
        current_step: int,
        **kwargs,
    ):
        super().__init__(
            orientation="horizontal",
            spacing=10,
            size_hint_y=0.1,
            **kwargs,
        )

        for index, step in enumerate(APP_STEPS):
            prefix = self._get_prefix(index, current_step)

            label = Label(
                text=f"{prefix} {step}",
            )

            self.add_widget(label)

    def _get_prefix(
        self,
        index: int,
        current_step: int,
    ) -> str:
        if index < current_step:
            return "[✓]"

        if index == current_step:
            return "[•]"

        return "[ ]"