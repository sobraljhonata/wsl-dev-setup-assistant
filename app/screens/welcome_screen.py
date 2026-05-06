from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class WelcomeScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)

        self.app = app_ref

        platform_info = self.app.platform_service.get_platform_info()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12,
        )

        title = Label(
            text="[b]WSL Dev Setup Assistant[/b]",
            markup=True,
            font_size=28,
            size_hint_y=0.18,
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
            size_hint_y=0.32,
        )

        platform_text = self._get_platform_message(platform_info)

        self.platform_label = Label(
            text=platform_text,
            halign="center",
            valign="middle",
            size_hint_y=0.22,
        )

        explanation = Label(
            text=(
                "O objetivo não é esconder o Linux,\n"
                "mas ajudar você a aprender Linux com segurança."
            ),
            italic=True,
            size_hint_y=0.12,
        )

        start_button = Button(
            text="Começar",
            size_hint=(0.4, 0.14),
            pos_hint={"center_x": 0.5},
            disabled=not platform_info.is_supported_for_launcher,
        )

        start_button.bind(on_press=self.go_next)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(self.platform_label)
        layout.add_widget(explanation)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def _get_platform_message(self, platform_info) -> str:
        if platform_info.is_windows:
            return (
                f"Ambiente detectado: Windows {platform_info.release}\n"
                "Este é o ambiente recomendado para usar o launcher."
            )

        if platform_info.is_wsl:
            return (
                "Ambiente detectado: WSL/Linux.\n"
                "Este launcher deve ser executado no Windows.\n"
                "Dentro do WSL, use o Dev Setup CLI diretamente."
            )

        if platform_info.is_linux:
            return (
                "Ambiente detectado: Linux.\n"
                "Este launcher foi pensado para preparar WSL no Windows."
            )

        return (
            f"Ambiente detectado: {platform_info.system}.\n"
            "Este launcher foi pensado para Windows com WSL."
        )

    def go_next(self, *_):
        self.manager.current = "wsl_check"