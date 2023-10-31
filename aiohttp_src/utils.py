import bcrypt
from aiohttp import web
from pydantic import ValidationError

from aiohttp_src.http_errors import get_http_error
from database.db_init import async_engine, create_tables, drop_tables


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def validate(model, data):
    try:
        return model.model_validate(data).model_dump(exclude_unset=True)
    except ValidationError as err:
        print(err.errors())
        error = err.errors()[0]
        error.pop("ctx", None)
        raise get_http_error(web.HTTPBadRequest, error)


async def orm_context(web: web.Application):
    print("Create tables")
    await create_tables(async_engine)
    yield
    await drop_tables(async_engine)
    print("Drop tables")
