import os

from flask import Flask
from flask_admin import Admin

admin = Admin(template_mode="bootstrap3")

def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions

    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    # register blueprints


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app