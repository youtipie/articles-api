from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from app.auth import bp
from app.users.models import User
from app.utils import with_validation


@bp.route("/login", methods=["POST"])
@with_validation({"email": str, "password": str})
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {"message": "Invalid email or password."}, 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}, 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}, 200
