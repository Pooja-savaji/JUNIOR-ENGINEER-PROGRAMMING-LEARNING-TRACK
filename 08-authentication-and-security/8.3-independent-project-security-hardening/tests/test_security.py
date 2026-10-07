import sys
sys.path.append("src")

from app import login, is_admin
def test_login():
    assert login("pooja", "1234") == True
    assert login("pooja", "wrong") == False

def test_admin_access():
    assert is_admin("admin") == True
    assert is_admin("pooja") == False
