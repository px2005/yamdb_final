from enum import Enum


class Roles(Enum):
    user = 'Аутентифицированный пользователь'
    moderator = 'Модератор'
    admin = 'Администратор'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
