from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK

from main import app

client = TestClient(app)


def test_root_view() -> None:
    # TODO: fake data
    name = "John"
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == HTTP_200_OK, response.text
    response_data = response.json()
    # assert "message" in response_data, response_data
    expected_message = f"Hello {name}"
    assert response_data["message"] == expected_message, response_data
