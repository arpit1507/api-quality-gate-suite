Feature: User Microservice Quality Gate
  As a system administrator
  I want to ensure the user REST API complies with data contracts and performance limits
  So that faulty deployments are blocked

  Scenario: Successfully fetch and validate user profile data
    Given the user microservice API is running
    When I send a GET request to "/api/users/1"
    Then the response status code should be 200
    And the response body should contain valid user schema fields
    And the response time should be under 500 milliseconds