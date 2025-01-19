from __future__ import annotations

import asyncio
from typing import Callable, Awaitable, Self, Generator


class RunWithTO[T]:
    __slots__ = ("coro", "_value", "timed_out", "args", "kwargs", "timeout_s")

    def __init__(self: Self, coro: Callable[[...], Awaitable[T]], timeout_s: float | int = 5) -> None:
        self.coro = coro
        self._value = None
        self.timed_out = False
        self.timeout_s = timeout_s
        self.args = tuple()
        self.kwargs = {}

    def __await__(self: Self) -> Generator[None, None, RunWithTO[T]]:
        return self.run().__await__()

    def __call__(self, *args, **kwargs) -> RunWithTO[T]:
        self.args = args
        self.kwargs = kwargs

        return self

    def __bool__(self: Self) -> bool:
        return self.timed_out

    async def run(self) -> RunWithTO[T]:
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.coro(*self.args, **self.kwargs))

        try:
            self._value = await asyncio.wait_for(task, timeout=self.timeout_s)
        except asyncio.TimeoutError:
            task.cancel()
            self.timed_out = True

        return self

    @property
    def value(self: Self) -> T:
        return self._value

