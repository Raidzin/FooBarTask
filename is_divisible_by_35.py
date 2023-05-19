import logging
from typing import Literal, TypeAlias

from fastapi import FastAPI, HTTPException, status
from httpx import post, HTTPError, get
from pydantic import BaseModel

app = FastAPI(title='Is divisible by 35')

ResultStr: TypeAlias = Literal['is_divisible_by_35']

IS_DIVISIBLE_BY_3_URL = 'http://is_divisible_by_3/is_divisible_by_3'
IS_DIVISIBLE_BY_5_URL = ('http://is_divisible_by_5/json/api/v8/nw/'
                         '{number}/div5yn')


class Number(BaseModel):
    value: int


@app.post('/is_divisible_by_35')
async def is_divisible_by_35(
        number: Number
) -> dict[ResultStr, bool]:
    try:
        is_divisible_by_3 = post(
            IS_DIVISIBLE_BY_3_URL,
            json={'value': number.value}
        ).json()['is_divisible_by_3']
        is_divisible_by_5 = get(
            IS_DIVISIBLE_BY_5_URL.format(
                number=number.value
            )
        ).json()
        return {
            'is_divisible_by_35': is_divisible_by_3 and is_divisible_by_5
        }
    except (HTTPError, KeyError) as error:
        logging.exception(type(error))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY
        )
