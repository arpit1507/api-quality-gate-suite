import time

import requests
from behave import given, when, then


@given("the user microservice API is running")
def step_api_is_running(context):
    context.base_url = "https://jsonplaceholder.typicode.com"

    response = requests.get(
        f"{context.base_url}/users/1",
        timeout=5,
    )

    assert response.status_code == 200, (
        f"User API is not available. "
        f"Status code: {response.status_code}"
    )


@when('I send a GET request to "/api/users/1"')
def step_send_get_request(context):
    # JSONPlaceholder is used as a temporary public mock API.
    # The path is translated to its equivalent endpoint.
    url = f"{context.base_url}/users/1"

    start_time = time.perf_counter()

    context.response = requests.get(
        url,
        timeout=5,
    )

    end_time = time.perf_counter()

    context.response_time_ms = (end_time - start_time) * 1000


@then("the response status code should be 200")
def step_status_code(context):
    assert context.response.status_code == 200, (
        f"Expected HTTP 200, "
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
def step_response_time(context):
    assert context.response_time_ms < 500, (
        f"Response took {context.response_time_ms:.2f} ms, "
        f"which exceeds the 500 ms limit"
    )