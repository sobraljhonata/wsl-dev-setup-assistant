from collections.abc import Callable
from threading import Thread
from typing import TypeVar

from kivy.clock import Clock

T = TypeVar("T")


class AsyncCommandService:
    def run(
        self,
        task: Callable[[], T],
        on_success: Callable[[T], None],
        on_error: Callable[[Exception], None],
    ) -> None:
        thread = Thread(
            target=self._execute,
            args=(task, on_success, on_error),
            daemon=True,
        )
        thread.start()

    def _execute(
        self,
        task: Callable[[], T],
        on_success: Callable[[T], None],
        on_error: Callable[[Exception], None],
    ) -> None:
        try:
            result = task()
            Clock.schedule_once(lambda _dt: on_success(result))
        except Exception as error:
            Clock.schedule_once(
                lambda _dt, captured_error=error: on_error(captured_error)
            )