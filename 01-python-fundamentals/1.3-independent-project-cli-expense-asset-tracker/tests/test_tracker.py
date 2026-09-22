from src.tracker import add_expense, total_expense
def test_add_expense():
    add_expense("Food", 100)
    assert total_expense() == 100

def test_invalid_amount():
    assert add_expense("Food", -50) == "Invalid amount"
