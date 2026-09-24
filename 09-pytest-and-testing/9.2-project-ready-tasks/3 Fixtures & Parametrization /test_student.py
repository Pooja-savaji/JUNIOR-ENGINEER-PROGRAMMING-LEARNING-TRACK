from student import is_pass
def test_marks(marks):
    assert is_pass(marks[0]) is False
    assert is_pass(marks[1]) is True
    assert is_pass(marks[2]) is True
    assert is_pass(marks[3]) is True
