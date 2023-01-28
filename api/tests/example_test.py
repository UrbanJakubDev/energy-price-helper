from app import create_app
import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)


app = create_app()


def test_app():
    assert app.config['FLASK_ENV'] == 'development'

