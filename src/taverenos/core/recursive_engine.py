"""Depth-limited recursive execution utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar

TContext = TypeVar("TContext")
TResult = TypeVar("TResult")


class RecursionGuardError(RuntimeError):
    """Raised when recursive execution exceeds the configured depth."""


Continuation = Callable[[Callable[..., TResult], Optional[TContext]], TResult]
ExecutorFn = Callable[[TContext, Continuation], TResult]


@dataclass
class RecursiveExecutor(Generic[TContext, TResult]):
    """Executes a recursive task with built-in depth protection."""

    executor: ExecutorFn[TContext, TResult]
    max_depth: int = 5

    def run(self, context: TContext) -> TResult:
        return self._step(context, depth=0)

    def _step(self, context: TContext, depth: int) -> TResult:
        if depth > self.max_depth:
            raise RecursionGuardError(
                f"Maximum recursion depth {self.max_depth} exceeded at depth {depth}"
            )

        def continuation(next_executor: ExecutorFn[TContext, TResult], next_context: Optional[TContext] = None) -> TResult:
            return self._branch(next_executor, next_context if next_context is not None else context, depth + 1)

        return self.executor(context, continuation)

    def _branch(self, executor: ExecutorFn[TContext, TResult], context: TContext, depth: int) -> TResult:
        branch = RecursiveExecutor(executor=executor, max_depth=self.max_depth)
        return branch._step(context, depth)  # pylint: disable=protected-access


__all__ = ["RecursionGuardError", "RecursiveExecutor"]
