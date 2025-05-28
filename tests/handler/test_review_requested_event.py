import pytest
from flask import Flask
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

import app.handler.review_requested_event as review_requested_handler


@pytest.fixture
def client() -> FlaskClient:
    app = Flask(__name__)
    app.register_blueprint(review_requested_handler.review_requested_bp)
    return app.test_client()


def test_review_requested_event_no_data(client: FlaskClient) -> None:
    response = client.post(
        "/webhook/review_requested",
        json={},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "No data received"}


def test_review_requested_event_with_data(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    data = {"key": "value"}
    mock_process_review_requested_event = mocker.patch.object(
        review_requested_handler,
        "process_review_requested_event",
        return_value=("Review request event processed", 200),
    )

    response = client.post(
        "/webhook/review_requested",
        json=data,
    )

    mock_process_review_requested_event.assert_called_once_with(data)

    assert response.status_code == 200
    assert response.get_json() == {"message": "Review request event processed"}
