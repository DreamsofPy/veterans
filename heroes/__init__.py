
from flask import Flask
import settings

app = Flask('heroes')
app.config.from_object('heroes.settings')

import views

if __name__ == "__main__":
    app.run()
