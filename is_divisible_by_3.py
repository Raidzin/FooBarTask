from typing import Literal, TypeAlias

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

ResultStr: TypeAlias = Literal['is_divisible_by_3']


class Numer(BaseModel):
    value: int


@app.post('/is_divisible_by_3')
async def is_divisible_by_3(
        number: Numer
) -> dict[ResultStr, bool]:
    return {
        'is_divisible_by_3': number.value % 3 == 0
    }
