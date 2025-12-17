"""Tests for tty module."""

from hearts_engine.tty import SupportsTTY
from hearts_engine.tty import format


class DescribeSupportsTTY:
    """Tests for the SupportsTTY protocol."""

    def it_is_runtime_checkable(self) -> None:
        class HasTTY:
            def __tty__(self) -> str:
                return "colored"

        class NoTTY:
            pass

        assert isinstance(HasTTY(), SupportsTTY)
        assert not isinstance(NoTTY(), SupportsTTY)


class DescribeFormat:
    """Tests for the format function."""

    def it_returns_str_when_tty_false(self) -> None:
        class Obj:
            def __str__(self) -> str:
                return "plain"

            def __tty__(self) -> str:
                return "colored"

        assert format(Obj(), tty=False) == "plain"

    def it_returns_tty_when_tty_true(self) -> None:
        class Obj:
            def __str__(self) -> str:
                return "plain"

            def __tty__(self) -> str:
                return "colored"

        assert format(Obj(), tty=True) == "colored"

    def it_falls_back_to_str_when_no_tty_method(self) -> None:
        class PlainObj:
            def __str__(self) -> str:
                return "plain only"

        assert format(PlainObj(), tty=True) == "plain only"
        assert format(PlainObj(), tty=False) == "plain only"

    def it_works_with_builtin_types(self) -> None:
        assert format(42, tty=True) == "42"
        assert format("hello", tty=False) == "hello"
