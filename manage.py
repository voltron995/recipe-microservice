#!/usr/bin/env python3
from application.app import manager, app, db
from application import models, urls


if __name__ == "__main__":
    manager.run()
