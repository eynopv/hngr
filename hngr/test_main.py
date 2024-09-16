from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


def test_index_loads():
    response = client.get("/")
    assert response.status_code == 200


def test_service_worker_loads():
    response = client.get("/service-worker.js")
    assert response.status_code == 200


def test_scrape():
    response = client.post("/scrape", data={"link": "mock"}, follow_redirects=False)
    assert response.status_code == 303


def test_scrape_invalidsource():
    response = client.post("/scrape", data={"link": "invalidsource.com"})
    assert response.status_code == 400
    assert "text/html" in response.headers.get("content-type")


def test_recipe_loads():
    response = client.get("/recipe/101")
    assert response.status_code == 200


def test_recipe_delete_non_existant():
    response = client.delete("/recipe/999")
    assert response.status_code == 404


def test_recipe_delete():
    response = client.delete("/recipe/100")
    assert response.status_code == 204


def test_search():
    response = client.post("/search", data={"term": "test"})
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type")


def test_new_recipe_loads():
    response = client.get("/new-recipe")
    assert response.status_code == 200


def test_new_recipe_edit_loads():
    response = client.get("/new-recipe/edit")
    assert response.status_code == 200


def test_new_recipe_create():
    response = client.post(
        "/new-recipe/edit",
        data={
            "name": "Test name",
            "description": "Test description",
            "directions": "Test directions",
            "ingredients": "Test ingredients",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303


def test_new_recipe_create_with_empty_description():
    response = client.post(
        "/new-recipe/edit",
        data={
            "name": "Test name",
            "description": "",
            "directions": "Test directions",
            "ingredients": "Test ingredients",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303


def test_api_list_recipes():
    response = client.get("/api/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert "data" in recipes
    assert len(recipes["data"]) > 0
