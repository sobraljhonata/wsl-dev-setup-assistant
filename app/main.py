from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from app.screens.distro_screen import DistroScreen
from app.screens.terminal_screen import TerminalScreen
from app.screens.welcome_screen import WelcomeScreen
from app.screens.wsl_check_screen import WslCheckScreen
from app.services.async_command_service import AsyncCommandService
from app.services.devsetup_service import DevSetupService
from app.services.wsl_service import WslService


class DevSetupLauncherApp(App):
    def build(self):
        self.title = "WSL Dev Setup Assistant"

        self.wsl_service = WslService()
        self.devsetup_service = DevSetupService(self.wsl_service)
        self.async_command_service = AsyncCommandService()

        self.selected_distro = "Ubuntu-24.04"

        sm = ScreenManager()

        sm.add_widget(
            WelcomeScreen(
                name="welcome",
            )
        )

        sm.add_widget(
            WslCheckScreen(
                app_ref=self,
                name="wsl_check",
            )
        )

        sm.add_widget(
            DistroScreen(
                app_ref=self,
                name="distro",
            )
        )

        sm.add_widget(
            TerminalScreen(
                app_ref=self,
                name="terminal",
            )
        )

        return sm


if __name__ == "__main__":
    DevSetupLauncherApp().run()