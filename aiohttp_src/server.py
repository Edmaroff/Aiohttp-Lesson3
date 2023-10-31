# --------------------------------------------------
# Первый вариант кода
# --------------------------------------------------
# from aiohttp import web
#
# from aiohttp_src.schema import CreateUser, PatchUser, CreateAdvertisement, PatchAdvertisement
# from aiohttp_src.utils import hash_password, validate
# from database.crud import add_user, delete_user, get_user_by_id, update_user, add_advert, \
#     get_advert_by_id, update_advert, delete_advert
# from database.db_init import async_session
#
#
#
# class UserView(web.View):
#     @property
#     def user_id(self):
#         return int(self.request.match_info["user_id"])
#
#     async def get(self):
#         user = await get_user_by_id(async_session, self.user_id)
#         return web.json_response(user.to_dict)
#
#     async def post(self):
#         user_data = await validate(CreateUser, await self.request.json())
#         user_data["password"] = hash_password(user_data.get("password"))
#         user = await add_user(async_session, user_data)
#         return web.json_response({"id": user.id})
#
#     async def patch(self):
#         user_data = await validate(PatchUser, await self.request.json())
#         user = await get_user_by_id(async_session, self.user_id)
#         if "password" in user_data:
#             user_data["password"] = hash_password(user_data["password"])
#         user = await update_user(async_session, user, user_data)
#         return web.json_response({"id": user.id})
#
#     async def delete(self):
#         user = await get_user_by_id(async_session, self.user_id)
#         await delete_user(async_session, user)
#         return web.json_response({"status": "ok"})
#
#
# class AdvertView(web.View):
#     @property
#     def advert_id(self):
#         return int(self.request.match_info["advert_id"])
#
#
#     async def get(self):
#         advert = await get_advert_by_id(async_session, self.advert_id)
#         return web.json_response(advert.to_dict)
#
#     async def post(self):
#         advert_data = await validate(CreateAdvertisement, await self.request.json())
#         advert = await add_advert(async_session, advert_data)
#         return web.json_response({"id": advert.id})
#
#     async def patch(self):
#         advert_data = await validate(PatchAdvertisement, await self.request.json())
#         advert = await get_advert_by_id(async_session, self.advert_id)
#         advert = await update_advert(async_session, advert, advert_data)
#         return web.json_response({"id": advert.id})
#
#     async def delete(self):
#         advert = await get_advert_by_id(async_session, self.advert_id)
#         await delete_advert(async_session, advert)
#         return web.json_response({"status": "ok"})

# --------------------------------------------------
# Второй вариант кода
# --------------------------------------------------
from aiohttp import web

from aiohttp_src.schema import (
    CreateAdvertisement,
    CreateUser,
    PatchAdvertisement,
    PatchUser,
)
from aiohttp_src.utils import hash_password, validate
from database.crud import AdvertisementHandler, UserHandler
from database.db_init import async_session


class UserView(web.View):
    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        handler = UserHandler(async_session)
        user = await handler.get_object_by_id(self.user_id)
        return web.json_response(user.to_dict)

    async def post(self):
        user_data = await validate(CreateUser, await self.request.json())
        user_data["password"] = hash_password(user_data.get("password"))
        handler = UserHandler(async_session)
        user = await handler.add_object(user_data)
        return web.json_response({"id": user.id})

    async def patch(self):
        user_data = await validate(PatchUser, await self.request.json())
        handler = UserHandler(async_session)
        user = await handler.get_object_by_id(self.user_id)
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])
        user = await handler.update_object(user, user_data)
        return web.json_response({"id": user.id})

    async def delete(self):
        handler = UserHandler(async_session)
        user = await handler.get_object_by_id(self.user_id)
        await handler.delete_object(user)
        return web.json_response({"status": "ok"})


class AdvertView(web.View):
    @property
    def advert_id(self):
        return int(self.request.match_info["advert_id"])

    async def get(self):
        handler = AdvertisementHandler(async_session)
        advert = await handler.get_object_by_id(self.advert_id)
        return web.json_response(advert.to_dict)

    async def post(self):
        advert_data = await validate(CreateAdvertisement, await self.request.json())
        handler = AdvertisementHandler(async_session)
        advert = await handler.add_object(advert_data)
        return web.json_response({"id": advert.id})

    async def patch(self):
        advert_data = await validate(PatchAdvertisement, await self.request.json())
        handler = AdvertisementHandler(async_session)
        advert = await handler.get_object_by_id(self.advert_id)
        advert = await handler.update_object(advert, advert_data)
        return web.json_response({"id": advert.id})

    async def delete(self):
        handler = AdvertisementHandler(async_session)
        advert = await handler.get_object_by_id(self.advert_id)
        await handler.delete_object(advert)
        return web.json_response({"status": "ok"})
