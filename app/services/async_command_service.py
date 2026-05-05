from collections.abc import Callable
from threading import Thread

from kivy.clock import Clock

from app.domain.command_result import CommandResult


class AsyncCommandService:
    def run(
        self,
        task: Callable[[], CommandResult],
        on_success: Callable[[CommandResult], None],
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
        task: Callable[[], CommandResult],
        on_success: Callable[[CommandResult], None],
        on_error: Callable[[Exception], None],
    ) -> None:
        try:
            result = task()
            Clock.schedule_once(lambda _dt: on_success(result))
        except Exception as error:
            Clock.schedule_once(
                lambda _dt, captured_error=error: on_error(captured_error)
            )