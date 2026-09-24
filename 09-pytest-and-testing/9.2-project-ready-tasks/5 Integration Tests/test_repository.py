from database import create_database
from repository import save_user, get_user

def test_save_and_get_user():
    connection = create_database()
    save_user(connection, "Pooja")
    user = get_user(connection, 1)
    assert user[0] == "Pooja"
