from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def get_user(self):
        pass


class MySQLRepository(UserRepository):
    def get_user(self):
        return "User from MySQL"


class FileRepository(UserRepository):
    def get_user(self):
        return "User from File"


print(MySQLRepository().get_user())
print(FileRepository().get_user())
