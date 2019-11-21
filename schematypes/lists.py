#!/usr/bin/env python
# coding: utf-8

from .schemas import List, Dict
from .strings import Uri, String

class ListofList(List, additionalProperties=List.__schema__):
    ...


class ListofDict(List, additionalProperties=Dict.__schema__):
    ...


class ListofUri(List, items=Uri.__schema__, minItems=1):
    def text(x):
        return aiorun(x.gather(json=False))

    def json(x):
        return aiorun(x.gather())

    async def one(self, session, url, json=True):
        async with session.get(url) as response:
            return await response.json() if json else response.text()

    async def gather(x, json=True):
        async with __import__("aiohttp").ClientSession() as session:
            return await __import__("asyncio").gather(
                *(x.one(session, _, json) for _ in x)
            )


def aiorun(object):
    try:
        return __import__("asyncio").run(object)
    except RuntimeError as e:
        if "nest_asyncio" not in sys.modules:
            __import__("nest_asyncio").apply()
            return aiorun(object)
        else:
            raise e
