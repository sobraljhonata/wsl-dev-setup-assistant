from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager

from app.config.settings import (
    APP_NAME,
    DEFAULT_DISTRO,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
)
from app.screens.distro_screen import DistroScreen
from app.screens.terminal_screen import TerminalScreen
from app.screens.welcome_screen import WelcomeScreen
from app.screens.wsl_check_screen import WslCheckScreen
from app.services.async_command_service import AsyncCommandService
from app.services.devsetup_service import DevSetupService
from app.services.platform_service import PlatformService
from app.services.wsl_service import WslService
from app.screens.first_run_screen import FirstRunScreen

Config.set("graphics", "width", str(DEFAULT_WINDOW_WIDTH))
Config.set("graphics", "height", str(DEFAULT_WINDOW_HEIGHT))
Config.set("graphics", "resizable", "1")


class DevSetupLauncherApp(App):
    def build(self):
        self.title = APP_NAME

        self.wsl_service = WslService()
        self.devsetup_service = DevSetupService(self.wsl_service)
        self.async_command_service = AsyncCommandService()
        self.platform_service = PlatformService()

        self.selected_distro = DEFAULT_DISTRO

        sm = ScreenManager()

        sm.add_widget(
            WelcomeScreen(
                app_ref=self,
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
        
        sm.add_widget(
            FirstRunScreen(
                app_ref=self,
                name="first_run",
            )
        )

        return sm


if __name__ == "__main__":
    DevSetupLauncherApp().run()