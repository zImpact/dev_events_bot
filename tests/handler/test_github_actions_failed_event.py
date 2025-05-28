import pytest
from flask import Flask
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

import app.handler.github_actions_failed_event as github_actions_failed_handler


@pytest.fixture
def client() -> FlaskClient:
    app = Flask(__name__)
    app.register_blueprint(github_actions_failed_handler.actions_bp)
    return app.test_client()


def test_github_actions_failed_event_no_data(client: FlaskClient) -> None:
    response = client.post(
        "/webhook/github_actions",
        json={},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "No data received"}


def test_github_actions_failed_event_with_data(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    data = {"key": "value"}
    mock_process_github_actions_failed_event = mocker.patch.object(
        github_actions_failed_handler,
        "process_github_actions_failed_event",
        return_value=("Workflow completed successfully", 200),
    )

    response = client.post(
        "/webhook/github_actions",
        json=data,
    )

    mock_process_github_actions_failed_event.assert_called_once_with(data)

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Workflow completed successfully"
    }
