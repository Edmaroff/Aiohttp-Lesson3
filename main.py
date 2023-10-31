from aiohttp import web

from aiohttp_src.server import AdvertView, UserView
from aiohttp_src.utils import orm_context


def main():
    app = web.Application()
    app.cleanup_ctx.append(orm_context)

    app.add_routes(
        [
            web.get("/users/{user_id:\d+}", UserView),
            web.patch("/users/{user_id:\d+}", UserView),
            web.delete("/users/{user_id:\d+}", UserView),
            web.post("/users", UserView),
            web.get("/advertisement/{advert_id:\d+}", AdvertView),
            web.patch("/advertisement/{advert_id:\d+}", AdvertView),
            web.delete("/advertisement/{advert_id:\d+}", AdvertView),
            web.post("/advertisement", AdvertView),
        ]
    )
    web.run_app(app)


if __name__ == "__main__":
    main()
