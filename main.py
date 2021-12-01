import sys

from src.gunicorn_app import app


if __name__ == "__main__":
    sys.exit(app())
