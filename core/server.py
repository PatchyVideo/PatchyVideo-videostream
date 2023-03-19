from fastapi import FastAPI
from pydantic import BaseModel

from core.url_operator import match_operator

server = FastAPI()


class infoModel(BaseModel):
    url: str


@server.post("/")
async def root(info: infoModel):
    operator = match_operator(info.url)
    if operator is None:
        return {'error': 'No suitable operator found'}

    return await operator.main(info.url)
