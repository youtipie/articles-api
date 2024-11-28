from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .config import Config

# from .docs import spec

db = SQLAlchemy()
jwt = JWTManager()


# swagger = Swagger(template=spec)


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SWAGGER"] = {
        "openapi": "3.0.3"
    }
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    # swagger.init_app(app)

    from .commands import bp as commands_bp
    app.register_blueprint(commands_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .users import bp as users_bp
    app.register_blueprint(users_bp)

    from .article import bp as article_bp
    app.register_blueprint(article_bp)


    with app.app_context():
        app.cached_roles = {role.name.lower(): role for role in db.session.query(user_models.Role).all()}

    return app


from .users import models as user_models
from .article import models
