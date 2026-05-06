import os
import platform
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformInfo:
    system: str
    release: str
    python_version: str
    is_windows: bool
    is_linux: bool
    is_wsl: bool

    @property
    def is_supported_for_launcher(self) -> bool:
        return self.is_windows


class PlatformService:
    def get_platform_info(self) -> PlatformInfo:
        system = platform.system()
        release = platform.release()

        return PlatformInfo(
            system=system,
            release=release,
            python_version=sys.version.split()[0],
            is_windows=self.is_windows(),
            is_linux=self.is_linux(),
            is_wsl=self.is_wsl(),
        )

    def is_windows(self) -> bool:
        return platform.system().lower() == "windows"

    def is_linux(self) -> bool:
        return platform.system().lower() == "linux"

    def is_wsl(self) -> bool:
        if not self.is_linux():
            return False

        if "WSL_DISTRO_NAME" in os.environ:
            return True

        try:
            with open("/proc/version", encoding="utf-8") as file:
                content = file.read().lower()
                return "microsoft" in content or "wsl" in content
        except FileNotFoundError:
            return False