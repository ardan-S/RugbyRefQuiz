from flask import Flask
from flask_session import Session
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Session(app)

    from app import routes
    app.register_blueprint(routes.bp)

    return app


app = create_app()
