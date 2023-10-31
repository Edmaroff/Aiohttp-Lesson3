import asyncio

import aiohttp


async def main():
    url_user = "http://127.0.0.1:8080/users"
    url_ad = "http://127.0.0.1:8080/advertisement"

    async with aiohttp.ClientSession() as session:
        # # REST для пользователей
        # # POST - создать пользователя
        async with session.post(
            url_user,
            json={"name": "user_1", "password": "password"},
            headers={"Authorization": "some_token"},
        ) as response:
            print(response.status)
            print(await response.text())
        #
        # # GET - получить пользователя
        # async with session.get(url_user + "/1") as response:
        #     print(response.status)
        #     print(await response.text())

        # # PATCH - изменить пользователя
        # async with session.patch(
        #     url_user + "/1", json={"name": "1", "password": "password2"}
        # ) as response:
        #     print(response.status)
        #     print(await response.text())
        #
        # # DELETE - удалить пользователя
        # async with session.delete(url_user + "/1") as response:
        #     print(response.status)
        #     print(await response.text())
        #
        # # REST для объявлений
        # # POST - создать объявление
        # async with session.post(
        #     url_ad,
        #     json={"heading": "Заголовок 1", "description": "Описание 1", "owner_id": 1},
        #     headers={"Authorization": "some_token"},
        # ) as response:
        #     print(response.status)
        #     print(await response.text())
        #
        # # GET - получить объявление
        # async with session.get(url_ad + "/1") as response:
        #     print(response.status)
        #     print(await response.text())
        #
        # # PATCH - изменить объявление
        # async with session.patch(
        #     url_ad + "/5", json={"heading": "Заголовок 1-1", "owner_id": 1}
        # ) as response:
        #     print(response.status)
        #     print(await response.text())
        #
        # # DELETE - удалить объявление
        # async with session.delete(url_ad + "/1") as response:
        #     print(response.status)
        #     print(await response.text())


asyncio.run(main())
