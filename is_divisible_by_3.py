from typing import Literal, TypeAlias, Annotated
from uuid import uuid4

from fastapi import FastAPI, Depends
from fastapi.requests import Request
from pydantic import BaseModel

from structlogging import logger

app = FastAPI(title='Is divisible by 3')

ResultStr: TypeAlias = Literal['is_divisible_by_3']

REQUEST_ID = 'X-Request-Id'


def get_request_id(request: Request):
    if REQUEST_ID in request.headers:
        return request.headers[REQUEST_ID]
    return str(uuid4())


RequestId: TypeAlias = Annotated[str, Depends(get_request_id)]


class Number(BaseModel):
    value: int


@app.post('/is_divisible_by_3')
async def is_divisible_by_3(
        number: Number,
        request_id: RequestId,
) -> dict[ResultStr, bool]:
    logger.info('REQUEST', number=number.value, request_id=request_id)
    return {
        'is_divisible_by_3': number.value % 3 == 0
    }
