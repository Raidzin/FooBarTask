from uuid import uuid4


from asyncio import create_task, gather
from typing import Literal, TypeAlias, Annotated

from fastapi import FastAPI, HTTPException, Request, Depends, status
from httpx import AsyncClient, HTTPError
from pydantic import BaseModel

from structlogging import logger

IS_DIVISIBLE_BY_3_URL = 'http://is_divisible_by_3/is_divisible_by_3'
IS_DIVISIBLE_BY_5_URL = ('http://is_divisible_by_5/json/api/v8/nw/'
                         '{number}/div5yn')
IS_DIVISIBLE_BY_35_URL = 'http://is_divisible_by_35/is_divisible_by_35'

app = FastAPI(title='Is divisible by')

Result: TypeAlias = Literal[0, 3, 5, 35]

NUMBERS_MAP: dict[int, Result] = {0: 35, 1: 3, 2: 5}

REQUEST_ID = 'X-Request-Id'


def get_request_id(request: Request):
    if REQUEST_ID in request.headers:
        return request.headers[REQUEST_ID]
    return str(uuid4())


RequestId: TypeAlias = Annotated[str, Depends(get_request_id)]


async def is_divisible_by_3(number: int, request_id) -> bool:
    async with AsyncClient() as client:
        try:
            return (await client.post(
                url=IS_DIVISIBLE_BY_3_URL,
                json={'value': number},
                headers={REQUEST_ID: request_id},
                timeout=60,
            )).json()['is_divisible_by_3']
        except (HTTPError, KeyError) as error:
            logger.exception(error)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY
            )


async def is_divisible_by_5(number: int, request_id) -> bool:
    async with AsyncClient() as client:
        try:
            return (await client.get(
                url=IS_DIVISIBLE_BY_5_URL.format(number=number),
                headers={REQUEST_ID: request_id},
                timeout=60,
            )).json()
        except HTTPError as error:
            logger.exception(error)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY
            )


async def is_divisible_by_35(number: int, request_id) -> bool:
    """А что, я его зря писал что ли?!"""
    async with AsyncClient() as client:
        try:
            return (await client.post(
                url=IS_DIVISIBLE_BY_35_URL,
                json={'value': number},
                headers={REQUEST_ID: request_id},
                timeout=60,
            )).json()['is_divisible_by_35']
        except (HTTPError, KeyError) as error:
            logger.exception(error)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY
            )


async def is_divisible_by(number: int, request_id) -> Result:
    tasks = [
        create_task(is_divisible_by_35(number, request_id)),
        create_task(is_divisible_by_3(number, request_id)),
        create_task(is_divisible_by_5(number, request_id)),
    ]
    results = await gather(*tasks)
    for key, result in enumerate(results):
        if result:
            return NUMBERS_MAP[key]
    return 0


class Numbers(BaseModel):
    values: list[int]


@app.post('/is_divisible_by')
async def is_divisible_by_3535(
        numbers: Numbers,
        request_id: RequestId,
) -> list[Result]:
    logger.info('REQUEST', numbers=numbers.values, request_id=request_id)
    tasks = [
        create_task(is_divisible_by(number, request_id))
        for number in numbers.values
    ]
    return await gather(*tasks)
