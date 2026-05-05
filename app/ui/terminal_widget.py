from collections.abc import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class TerminalWidget(BoxLayout):
    def __init__(
        self,
        on_execute: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(orientation="vertical", **kwargs)

        self.on_execute = on_execute

        self.output = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=0.8,
        )

        self.command_input = TextInput(
            multiline=False,
            hint_text="Digite um comando ou use os botões sugeridos...",
            size_hint_y=0.1,
        )

        self.execute_button = Button(
            text="Executar comando",
            size_hint_y=0.1,
        )

        self.execute_button.bind(on_press=self._handle_execute)

        self.add_widget(self.output)
        self.add_widget(self.command_input)
        self.add_widget(self.execute_button)

    def append_output(self, text: str) -> None:
        self.output.text += f"{text}\n"

    def set_command(self, command: str) -> None:
        self.command_input.text = command

    def _handle_execute(self, *_args) -> None:
        command = self.command_input.text.strip()

        if command:
            self.on_execute(command)