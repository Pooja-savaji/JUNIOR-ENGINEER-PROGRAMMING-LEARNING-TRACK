from validator import is_valid_age

def test_valid_age():
    assert is_valid_age(20) is True

def test_invalid_age():
    assert is_valid_age(15) is False
