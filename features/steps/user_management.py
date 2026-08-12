import time

import requests
from behave import given, when, then


BASE_URL = "https://jsonplaceholder.typicode.com"


@given("the user microservice API is running")
def step_api_is_running(context):
    """
    Verify that the public test API is reachable.
    """
    context.base_url = BASE_URL

    response = requests.get(
        f"{context.base_url}/users/1",
        timeout=5,
    )

    assert response.status_code == 200, (
        f"API health check failed: "
        f"expected 200, got {response.status_code}"
    )


@when('I send a GET request to "/api/users/1"')
def step_send_get_request(context):
    """
    Send a GET request and measure response time.
    """
    url = f"{context.base_url}/users/1"

    start = time.perf_counter()

    context.response = requests.get(
        url,
        timeout=5,
    )

    end = time.perf_counter()

    context.response_time_ms = (end - start) * 1000


@then("the response status code should be 200")
def step_verify_status_code(context):
    assert context.response.status_code == 200, (
        f"Expected status 200, "
        f"got {context.response.status_code}"
    )


@then("the response body should contain valid user schema fields")
def step_validate_user_schema(context):
    body = context.response.json()

    required_fields = {
        "id",
        "name",
        "username",
        "email",
    }

    missing_fields = required_fields - body.keys()

    assert not missing_fields, (
        f"Missing required fields: {missing_fields}"
    )

    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
    assert isinstance(body["username"], str)
    assert isinstance(body["email"], str)


@then("the response time should be under 500 milliseconds")
def step_validate_response_time(context):
    assert context.response_time_ms < 500, (
        f"Response took "
        f"{context.response_time_ms:.2f} ms; "
        f"limit is 500 ms"
    )