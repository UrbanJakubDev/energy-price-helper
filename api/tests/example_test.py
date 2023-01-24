from app import create_app
import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)


def test_app():

    app = create_app()
    assert app.config['FLASK_ENV'] == 'development'


def test_file_get():

    app = create_app()
    client = app.test_client()

    response = client.get('/api/file')
    assert response.status_code == 200
    assert response.json['message'] == 'Here is you file..'
