import pytest
from bot.utils import validate_symbol, validate_side, validate_type, validate_positive_number


def test_symbol_validation():
    assert validate_symbol("btcusdt") == "BTCUSDT"
    try:
        validate_symbol("")
        assert False, "Expected ValueError for empty symbol"
    except ValueError:
        assert True


def test_side_validation():
    assert validate_side("buy") == "BUY"
    try:
        validate_side("hold")
        assert False, "Expected ValueError for invalid side"
    except ValueError:
        assert True


def test_type_validation():
    assert validate_type("market") == "MARKET"
    try:
        validate_type("random")
        assert False, "Expected ValueError for invalid type"
    except ValueError:
        assert True


def test_positive_number():
    assert validate_positive_number("qty", "1.5") == 1.5
    try:
        validate_positive_number("qty", "-1")
        assert False, "Expected ValueError for negative number"
    except ValueError:
        assert True