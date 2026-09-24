import pytest
from calculator import add, divide, is_even

def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 2) == 5

def test_divide_decimal():
    assert divide(5, 2) == 2.5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_even():
    assert is_even(4) is True

def test_odd():
    assert is_even(5) is False

def test_zero():
    assert is_even(0) is True
