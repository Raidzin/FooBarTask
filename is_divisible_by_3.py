from typing import Literal, TypeAlias

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Is divisible by 3')

ResultStr: TypeAlias = Literal['is_divisible_by_3']


class Number(BaseModel):
    value: int


@app.post('/is_divisible_by_3')
async def is_divisible_by_3(
        number: Number
) -> dict[ResultStr, bool]:
    return {
        'is_divisible_by_3': number.value % 3 == 0
    }
