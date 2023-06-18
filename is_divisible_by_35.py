import structlogging
from uuid import uuid4

from typing import Literal, TypeAlias, Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from httpx import post, HTTPError, get
from pydantic import BaseModel

from structlogging import logger

app = FastAPI(title='Is divisible by 35')

ResultStr: TypeAlias = Literal['is_divisible_by_35']

IS_DIVISIBLE_BY_3_URL = 'http://is_divisible_by_3/is_divisible_by_3'
IS_DIVISIBLE_BY_5_URL = ('http://is_divisible_by_5/json/api/v8/nw/'
                         '{number}/div5yn')

REQUEST_ID = 'X-Request-Id'


def get_request_id(request: Request):
    if REQUEST_ID in request.headers:
        return request.headers[REQUEST_ID]
    return str(uuid4())


RequestId: TypeAlias = Annotated[str, Depends(get_request_id)]


class Number(BaseModel):
    value: int


@app.post('/is_divisible_by_35')
async def is_divisible_by_35(
        number: Number,
        request_id: RequestId,
) -> dict[ResultStr, bool]:
    logger.info('REQUEST', number=number.value, request_id=request_id)
    try:
        is_divisible_by_3 = post(
            url=IS_DIVISIBLE_BY_3_URL,
            json={'value': number.value},
            headers={REQUEST_ID: request_id},
            timeout=60,
        ).json()['is_divisible_by_3']
        is_divisible_by_5 = get(
            url=IS_DIVISIBLE_BY_5_URL.format(number=number.value),
            headers={REQUEST_ID: request_id},
            timeout=60,
        ).json()
        return {
            'is_divisible_by_35': is_divisible_by_3 and is_divisible_by_5
        }
    except (HTTPError, KeyError) as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY
        )
