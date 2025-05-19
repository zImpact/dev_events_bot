import pytest
from flask import Flask
import app.handler.repo_update as repo_handler


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(repo_handler.update_repo_bp)
    return app.test_client()


def test_update_repo_succes(mocker, client):
    mock_repo_update = mocker.patch.object(repo_handler, "update_repository")

    response = client.post("/update_repo")
    mock_repo_update.assert_called_once()

    assert response.status_code == 200
    assert response.get_json() == {"message": "Repository updated"}


def test_update_repo_failure(mocker, client):
    mocker.patch.object(
        repo_handler, "update_repository", side_effect=Exception("Something went wrong")
    )

    response = client.post("/update_repo")

    assert response.status_code == 500
    assert response.get_json() == {"error": "Something went wrong"}
