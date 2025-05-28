import pytest
from flask import Flask
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

import app.handler.commit_event as commit_handler


@pytest.fixture
def client() -> FlaskClient:
    app = Flask(__name__)
    app.register_blueprint(commit_handler.commit_bp)
    return app.test_client()


def test_commit_event_no_data(client: FlaskClient) -> None:
    response = client.post(
        "/webhook/commits",
        json={},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "No data received"}


def test_commit_event_with_data(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    data = {"key": "value"}
    mock_process_commit_event = mocker.patch.object(
        commit_handler,
        "process_commit_event",
        return_value=("Commit event processed", 200),
    )

    response = client.post(
        "/webhook/commits",
        json=data,
    )

    mock_process_commit_event.assert_called_once_with(data)

    assert response.status_code == 200
    assert response.get_json() == {"message": "Commit event processed"}
