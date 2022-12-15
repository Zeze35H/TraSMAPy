from typing import Any, Callable


class Query:
    def __init__(self, queryFunc: Callable, tickInterval: int = 1) -> None:
        self._queryFunc: Callable = queryFunc
        self._tickInterval: int = tickInterval
        self._nextCall: int = 0  # ticks until next call

    def tick(self) -> bool:
        """Ticks the counter. Returns True if it is time to call the query."""
        self._nextCall -= 1
        return self._nextCall <= 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self._nextCall = self._tickInterval
        return self._queryFunc(*args, **kwds)
