import pytest

from taverenos.core import RecursionGuardError, RecursiveExecutor


def test_recursive_executor_halts_at_depth_limit() -> None:
    def executor(_: int, cont):
        return cont(executor, _ + 1)

    engine = RecursiveExecutor(executor=executor, max_depth=2)

    with pytest.raises(RecursionGuardError):
        engine.run(0)


def test_recursive_executor_returns_value() -> None:
    def executor(value: int, cont):
        if value >= 2:
            return value
        return cont(executor, value + 1)

    engine = RecursiveExecutor(executor=executor, max_depth=5)

    assert engine.run(0) == 2
