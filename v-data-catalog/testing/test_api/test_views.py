import pytest
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == HTTP_200_OK, response.text
    response_data = response.json()
    # assert "message" in response_data, response_data
    expected_message = "Hello World!"
    assert response_data["message"] == expected_message, response_data


@pytest.mark.parametrize(
    "name",
    [
        # TODO: fake data
        "John",
        "",
        "John Smith",
        "!@#$%^&",
    ],
)
def test_root_view_custom_name(
    name: str,
    client: TestClient,
) -> None:
    name = "John"
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == HTTP_200_OK, response.text
    response_data = response.json()
    # assert "message" in response_data, response_data
    expected_message = f"Hello {name}"
    assert response_data["message"] == expected_message, response_data
