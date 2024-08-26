import os
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .parsers import ParserFactory
from .db import Connection, list_recipes, create_recipe, retrieve_recipe

app = FastAPI()

app.mount("/static", StaticFiles(directory="hngr/static"), name="static")

templates = Jinja2Templates(directory="hngr/templates")

DATABASE_URL = os.environ.get("DATABASE_URL", "db/local.db")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    connection = Connection(url=DATABASE_URL)
    connection.open()
    recipes = list_recipes(connection)
    connection.close()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"recipes": recipes}
    )


@app.post("/scrape")
async def scrape(link: Annotated[str, Form()]):
    try:
        parser = ParserFactory.get_parser(link)
        new_recipe = parser.parse()
        if new_recipe:
            connection = Connection(url=DATABASE_URL)
            connection.open()
            recipe_id = create_recipe(connection, new_recipe)
            connection.close()
            return RedirectResponse(url=f"/recipe/{recipe_id}", status_code=303)
        raise Exception("something went wrong")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe(request: Request, recipe_id: int):
    connection = Connection(url=DATABASE_URL)
    connection.open()
    recipe = retrieve_recipe(connection, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail=f"recipe {recipe_id} not found")
    return templates.TemplateResponse(
        request=request, name="recipe.html", context={"recipe": recipe}
    )
