"""Entry-point for executing the application"""
from .app import app, db, manager
from . import urls


if __name__ == "__main__":

    app.run()
