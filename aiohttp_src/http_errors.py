import json
from typing import Type

from aiohttp import web


def get_http_error(error_class: Type[web.HTTPClientError], message):
    return error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )
