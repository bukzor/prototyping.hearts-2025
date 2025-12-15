"""Hearts engine tests."""

from hearts_engine import __doc__ as engine_doc


def test_engine_exists() -> None:
    """Verify engine module loads."""
    assert engine_doc is not None


def test_intentional_failure() -> None:
    """This test fails on purpose to verify CI catches failures."""
    assert False, "This failure is intentional - remove after CI verified"
