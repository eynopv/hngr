from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


def test_index_loads():
    response = client.get("/")
    assert response.status_code == 200


def test_scrape():
    response = client.post("/scrape", data={"link": "mock"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "Mock recipe",
        "description": "Description",
        "instructions": "First Step\nSecond Step\nThird Step",
        "ingredients": [
            {"name": "Ingredient with amount and unit", "amount": 2.0, "unit": "kg"},
            {"name": "Ingredient only with amount", "amount": 2.0, "unit": None},
            {"name": "Ingredient without amount and unit", "amount": None, "unit": None},
        ],
        "source": "mock",
    }


def test_scrape_invalidsource():
    response = client.post("/scrape", data={"link": "invalidsource.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "invalidsource.com is not supported"}
