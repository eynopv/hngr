from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Request

from .parsers import ParserFactory

app = FastAPI()


@app.get("/")
async def index():
    return {"Hello": "hngr"}


@app.post("/scrape")
async def scrape(link: Annotated[str, Form()]):
    try:
        parser = ParserFactory.get_parser(link)
        return parser.parse()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
