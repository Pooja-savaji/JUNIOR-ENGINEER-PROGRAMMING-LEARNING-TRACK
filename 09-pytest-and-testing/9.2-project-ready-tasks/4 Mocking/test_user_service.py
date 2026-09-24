from user_service import get_user

class FakeRepository:
    def get_user(self, user_id):
        return {"id": user_id, "name": "Pooja"}

def test_get_user():
    repository = FakeRepository()

    user = get_user(repository, 1)

    assert user["id"] == 1
    assert user["name"] == "Pooja"
