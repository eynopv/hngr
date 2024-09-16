import os
import logging
from typing import Annotated, Optional
from fastapi import FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from hngr.schemes import NewRecipe, Recipe

from .parsers import ParserFactory, clean_url
from .db import (
    Connection,
    list_recipes,
    create_recipe,
    retrieve_recipe,
    delete_recipe,
    search_recipes,
    update_recipe,
)
from .exceptions import ParserException


load_dotenv()

if os.environ.get("DEV", False):
    logging.basicConfig(level=logging.INFO)

DIRECTORY_STATIC = "hngr/static"
DIRECTORY_TEMPLATES = "hngr/templates"
DATABASE_URL = os.environ.get("DB", "")

app = FastAPI()


app.mount("/static", StaticFiles(directory=DIRECTORY_STATIC), name="static")

templates = Jinja2Templates(directory=DIRECTORY_TEMPLATES)


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


@app.get("/service-worker.js")
async def service_worker():
    headers = {"Cache-Control": "no-cache"}
    return FileResponse(f"{DIRECTORY_STATIC}/service-worker.js", headers=headers)


@app.post("/scrape")
# keep it synchonous because of playwright, ie BrowserLoader
def scrape(request: Request, response: Response, link: Annotated[str, Form()]):
    connection = Connection(url=DATABASE_URL)
    try:
        parser = ParserFactory.get_parser(clean_url(link))
        new_recipe = parser.parse()
        if new_recipe:
            connection.open()
            recipe_id = create_recipe(connection, new_recipe)
            recipe_url = f"/recipe/{recipe_id}/edit"
            if "hx-request" in request.headers:
                response.headers["HX-Redirect"] = recipe_url
                response.status_code = 303
                return response
            return RedirectResponse(url=recipe_url, status_code=303)
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


@app.get("/new-recipe", response_class=HTMLResponse)
async def new_recipe_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="new_recipe.html", context={"is_new": True}
    )


@app.get("/new-recipe/edit", response_class=HTMLResponse)
async def new_recipe_edit_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="edit_recipe.html", context={"is_new": True}
    )


@app.post("/new-recipe/edit")
async def new_recipe_create(
    request: Request,
    response: Response,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    directions: Annotated[str, Form()],
    ingredients: Annotated[str, Form()],
):
    connection = Connection(url=DATABASE_URL)
    try:
        new_recipe = NewRecipe(
            name=name,
            description=description,
            directions=directions,
            ingredients=ingredients,
            source="",
            image="",
        )
        connection.open()
        recipe_id = create_recipe(connection, new_recipe)
        recipe_url = f"/recipe/{recipe_id}"
        if "hx-request" in request.headers:
            response.headers["HX-Redirect"] = recipe_url
            response.status_code = 303
            return response
        return RedirectResponse(url=recipe_url, status_code=303)
    except Exception as e:
        logging.error(e)
        return HTMLResponse(
            content=f"<div class='error'>Internal server error: {str(e)}</div>", status_code=500
        )
    finally:
        connection.close()


@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe_page(request: Request, recipe_id: int):
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


@app.get("/recipe/{recipe_id}/edit")
async def edit_recipe_page(request: Request, recipe_id: int):
    connection = Connection(url=DATABASE_URL)
    try:
        connection.open()
        recipe = retrieve_recipe(connection, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail=f"recipe {recipe_id} not found")
        return templates.TemplateResponse(
            request=request, name="edit_recipe.html", context={"recipe": recipe}
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()


@app.post("/recipe/{recipe_id}/edit")
async def edit_recipe(
    request: Request,
    response: Response,
    recipe_id: int,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    directions: Annotated[str, Form()],
    ingredients: Annotated[str, Form()],
):
    connection = Connection(url=DATABASE_URL)
    try:
        connection.open()

        recipe = retrieve_recipe(connection, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail=f"recipe {recipe_id} not found")

        recipe.name = name
        recipe.description = description
        recipe.directions = directions
        recipe.ingredients = ingredients

        update_recipe(connection, recipe)

        recipe_url = f"/recipe/{recipe_id}"
        if "hx-request" in request.headers:
            response.headers["HX-Redirect"] = recipe_url
            response.status_code = 303
            return response
        return RedirectResponse(url=recipe_url, status_code=303)
    except Exception as e:
        logging.error(e)
        return HTMLResponse(
            content=f"<div class='error'>Internal server error: {str(e)}</div>", status_code=500
        )
    finally:
        connection.close()


@app.post("/search", status_code=200, response_class=HTMLResponse)
async def search(request: Request, term: Annotated[Optional[str], Form()] = None):
    connection = Connection(url=DATABASE_URL)
    try:
        connection.open()
        if term:
            recipes = search_recipes(connection, term)
        else:
            recipes = list_recipes(connection)
        return templates.TemplateResponse(
            request=request,
            name="partials/recipes_list.html",
            context={"recipes": recipes, "search": True},
        )
    finally:
        connection.close()
