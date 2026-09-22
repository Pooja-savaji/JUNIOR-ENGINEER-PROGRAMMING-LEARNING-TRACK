from src.order import Order
def test_create_order():
    order = Order("1", "Pooja", 500)
    assert order.customer == "Pooja"
    assert order.amount == 500
    assert order.status == "Pending"

def test_invalid_amount():
    try:
        Order("1", "Pooja", -100)
        assert False
    except ValueError:
        assert True
