import os
import logging
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from .parsers import ParserFactory, clean_url
from .db import Connection, list_recipes, create_recipe, retrieve_recipe, delete_recipe
from .exceptions import ParserException


load_dotenv()

if os.environ.get("DEV", False):
    logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.mount("/static", StaticFiles(directory="hngr/static"), name="static")

templates = Jinja2Templates(directory="hngr/templates")

DATABASE_URL = os.environ.get("DB", "")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    connection = Connection(url=DATABASE_URL)
    try:
        connection.open()
        recipes = list_recipes(connection)
        return templates.TemplateResponse(
            request=request, name="index.html", context={"recipes": recipes}
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()


@app.post("/scrape")
async def scrape(link: Annotated[str, Form()]):
    connection = Connection(url=DATABASE_URL)
    try:
        parser = ParserFactory.get_parser(clean_url(link))
        new_recipe = parser.parse()
        if new_recipe:
            connection.open()
            recipe_id = create_recipe(connection, new_recipe)
            return RedirectResponse(url=f"/recipe/{recipe_id}", status_code=303)
        raise Exception("something went wrong")
    except ValueError as e:
        return HTMLResponse(content=f"<div class='error'>{str(e)}</div>", status_code=400)
    except ParserException as e:
        return HTMLResponse(content=f"<div class='error'>{str(e)}</div>", status_code=400)
    except Exception as e:
        logging.error(e)
        return HTMLResponse(
            content=f"<div class='error'>Internal server error: {str(e)}</div>", status_code=500
        )
    finally:
        connection.close()


@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe(request: Request, recipe_id: int):
    connection = Connection(url=DATABASE_URL)
    try:
        connection.open()
        recipe = retrieve_recipe(connection, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail=f"recipe {recipe_id} not found")
        return templates.TemplateResponse(
            request=request, name="recipe.html", context={"recipe": recipe}
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()


@app.delete("/recipe/{recipe_id}", status_code=204)
async def recipe_delete(recipe_id: int):
    connection = Connection(url=DATABASE_URL)
    try:
        connection.open()
        is_deleted = delete_recipe(connection, recipe_id)
        if not is_deleted:
            raise HTTPException(status_code=404, detail=f"recipe {recipe_id} not found")
        return
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()
