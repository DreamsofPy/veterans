# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from flask.ext.script import Manager, Server
from heroes import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

if __name__ == "__main__":
    manager.run()

# from flask import Flask
# import settings

# app = Flask('heroes')
# app.config.from_object('heroes.settings')

# import views
