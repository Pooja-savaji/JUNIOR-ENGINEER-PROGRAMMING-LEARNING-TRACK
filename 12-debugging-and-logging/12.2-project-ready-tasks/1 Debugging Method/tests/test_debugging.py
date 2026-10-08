def test_total():
    price = 100
    quantity = 2

    assert price * quantity == 200

def test_average():
    numbers = [10, 20, 30]

    assert sum(numbers) / len(numbers) == 20

def test_user_exists():
    users = {
        1: {"name": "Pooja"},
        2: {"name": "Rahul"}
    }

    assert users[1]["name"] == "Pooja"

def test_discount():
    price = 1000
    discount = 0.20

    assert price - (price * discount) == 800
