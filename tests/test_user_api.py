import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


def test_user_not_found():
    """API should return 404 for a non-existent user."""

    response = requests.get(
        f"{BASE_URL}/users/999999",
        timeout=5,
    )

    assert response.status_code == 404


def test_valid_user_response():
    """A valid user should contain the expected fields."""

    response = requests.get(
        f"{BASE_URL}/users/1",
        timeout=5,
    )

    assert response.status_code == 200

    data = response.json()

    required_fields = {
        "id",
        "name",
        "username",
        "email",
    }

    assert required_fields.issubset(data.keys())


def test_user_id_has_correct_type():
    """User ID should be an integer."""

    response = requests.get(
        f"{BASE_URL}/users/1",
        timeout=5,
    )

    data = response.json()

    assert isinstance(data["id"], int)


def test_response_content_type():
    """API should return JSON content."""

    response = requests.get(
        f"{BASE_URL}/users/1",
        timeout=5,
    )

    content_type = response.headers.get("Content-Type", "")

    assert "application/json" in content_type


def test_response_contains_expected_header():
    """Verify that the API exposes a Content-Type header."""

    response = requests.get(
        f"{BASE_URL}/users/1",
        timeout=5,
    )

    assert "Content-Type" in response.headers


def test_malformed_payload_detection():
    """
    Demonstrate validation against an unexpected payload.

    JSONPlaceholder returns a valid user object, so we simulate
    receiving a malformed payload and validate it ourselves.
    """

    malformed_payload = {
        "id": "not-an-integer",
        "name": None,
    }

    assert not isinstance(malformed_payload["id"], int)
    assert malformed_payload["name"] is None