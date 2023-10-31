# --------------------------------------------------
# Первый вариант кода
# --------------------------------------------------

# from aiohttp import web
# from sqlalchemy.exc import IntegrityError
#
# from aiohttp_src.http_errors import get_http_error
#
# from .models import User, Advertisement
#
#
# async def get_user_by_id(session_maker, user_id: int) -> User:
#     async with session_maker() as session:
#         user = await session.get(User, user_id)
#     if user is None:
#         raise get_http_error(web.HTTPNotFound, f"User with id {user_id} not found")
#     return user
#
#
# async def add_user(session_maker, data: dict) -> User:
#     try:
#         async with session_maker() as session:
#             async with session.begin():
#                 user = User(**data)
#                 session.add(user)
#     except IntegrityError:
#         raise get_http_error(web.HTTPConflict, "User already exists")
#     return user
#
#
# async def update_user(session_maker, user: User, data: dict) -> User:
#     async with session_maker() as session:
#         async with session.begin():
#             for key, value in data.items():
#                 setattr(user, key, value)
#             session.add(user)
#     return user
#
#
# async def delete_user(session_maker, user: User):
#     async with session_maker() as session:
#         async with session.begin():
#             await session.delete(user)
#
#
# async def get_advert_by_id(session_maker, advert_id: int) -> Advertisement:
#     async with session_maker() as session:
#         advert = await session.get(Advertisement, advert_id)
#     if advert is None:
#         raise get_http_error(web.HTTPNotFound, f"Advertisement with id {advert_id} not found")
#     return advert
#
#
# async def add_advert(session_maker, data: dict) -> Advertisement:
#     try:
#         async with session_maker() as session:
#             async with session.begin():
#                 advert = Advertisement(**data)
#                 session.add(advert)
#     except IntegrityError:
#         raise get_http_error(web.HTTPNotFound, f"User with id {data.get('owner_id')} not found")
#     return advert
#
#
# async def update_advert(session_maker, advert: Advertisement, data: dict) -> Advertisement:
#     async with session_maker() as session:
#         async with session.begin():
#             for key, value in data.items():
#                 setattr(advert, key, value)
#             session.add(advert)
#     return advert
#
#
# async def delete_advert(session_maker, advert: Advertisement):
#     async with session_maker() as session:
#         async with session.begin():
#             await session.delete(advert)
#
#


# --------------------------------------------------
# Второй вариант кода
# --------------------------------------------------
from aiohttp import web
from sqlalchemy.exc import IntegrityError

from aiohttp_src.http_errors import get_http_error

from .models import Advertisement, User


class DatabaseObjectHandler:
    def __init__(self, session_maker, model):
        self.session_maker = session_maker
        self.model = model

    async def get_object_by_id(self, object_id: int):
        async with self.session_maker() as session:
            obj = await session.get(self.model, object_id)
        if obj is None:
            raise get_http_error(
                web.HTTPNotFound, f"{self.model.__name__} with id {object_id} not found"
            )
        return obj

    async def add_object(self, data: dict):
        try:
            async with self.session_maker() as session:
                async with session.begin():
                    obj = self.model(**data)
                    session.add(obj)
        except IntegrityError:
            if self.model == User:
                raise get_http_error(web.HTTPConflict, "User already exists")
            elif self.model == Advertisement:
                raise get_http_error(
                    web.HTTPNotFound, f"User with id {data.get('owner_id')} not found"
                )
        return obj

    async def update_object(self, obj, data: dict):
        try:
            async with self.session_maker() as session:
                async with session.begin():
                    for key, value in data.items():
                        setattr(obj, key, value)
                    session.add(obj)
                    return obj
        except IntegrityError:
            if self.model == Advertisement:
                raise get_http_error(
                    web.HTTPNotFound, f"User with id {data.get('owner_id')} not found"
                )

    async def delete_object(self, obj):
        async with self.session_maker() as session:
            async with session.begin():
                await session.delete(obj)


class UserHandler(DatabaseObjectHandler):
    def __init__(self, session_maker):
        super().__init__(session_maker, User)


class AdvertisementHandler(DatabaseObjectHandler):
    def __init__(self, session_maker):
        super().__init__(session_maker, Advertisement)
