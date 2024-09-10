from fastapi.testclient import TestClient
from playwright.sync_api import Page, expect

from .main import app


client = TestClient(app)


def test_index_loads(page: Page):
    page.goto(f"{client.base_url}/")
    expect(page).to_have_title("hngr")
    expect(page.get_by_role("heading", name="Welcome to hngr", level=1)).to_be_visible()


def test_scrape():
    response = client.post("/scrape", data={"link": "mock"}, follow_redirects=False)
    assert response.status_code == 303


def test_scrape_invalidsource():
    response = client.post("/scrape", data={"link": "invalidsource.com"})
    assert response.status_code == 400
    assert "text/html" in response.headers.get("content-type")


def test_recipe_loads():
    response = client.get("/recipe/1")
    assert response.status_code == 200


def test_recipe_delete_non_existant():
    response = client.delete("/recipe/999")
    assert response.status_code == 404


def test_recipe_delete():
    response = client.delete("/recipe/1")
    assert response.status_code == 204


def test_search():
    response = client.post("/search", data={"term": "test"})
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type")
