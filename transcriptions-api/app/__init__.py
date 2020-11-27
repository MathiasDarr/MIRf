import os
from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from app.uploads.views import uploads_blueprint

admin = Admin(template_mode="bootstrap3")


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    CORS(app)
    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions

    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    # register blueprints
    app.register_blueprint(uploads_blueprint)


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
