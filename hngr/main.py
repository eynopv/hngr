from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .parsers import ParserFactory
from .db import Connection, list_recipes, create_recipe

app = FastAPI()

templates = Jinja2Templates(directory="hngr/templates")

DATABASE_URL = "db/local.db"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    connection = Connection(url=DATABASE_URL)
    connection.open()
    recipes = list_recipes(connection)
    connection.close()
    print(recipes)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"recipes": recipes}
    )


@app.post("/scrape")
async def scrape(link: Annotated[str, Form()]):
    try:
        parser = ParserFactory.get_parser(link)
        new_recipe = parser.parse()
        print(new_recipe)
        if new_recipe:
            connection = Connection(url=DATABASE_URL)
            connection.open()
            create_recipe(connection, new_recipe)
            connection.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
