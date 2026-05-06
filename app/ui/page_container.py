from kivy.uix.boxlayout import BoxLayout


class PageContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=20,
            spacing=12,
            **kwargs,
        )