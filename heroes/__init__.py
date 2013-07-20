
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import settings

app = Flask('heroes')
app.config.from_object('heroes.settings')

from . import views

if __name__ == "__main__":
    app.run()
