import pytest
from src.discount import calculate_discount

def test_normal_discount():
    assert calculate_discount(100, 20) == 80

def test_full_discount():
    assert calculate_discount(100, 100) == 0

def test_invalid_discount():
    with pytest.raises(ValueError):
        calculate_discount(100, 120)
