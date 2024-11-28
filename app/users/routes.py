from flask import current_app, request

from app import db
from app.users import bp
from app.users.models import User
from app.utils import with_auth, with_validation


@bp.route("/roles", methods=["GET"])
def get_roles():
    return [role.to_dict() for role in current_app.cached_roles.values()]


@bp.route("", methods=["GET"])
@with_auth
def get_users():
    username = request.args.get("username")

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        return {"message": "Page number must be int value!"}

    page_size = current_app.config["PAGE_SIZE"]

    users_query = db.session.query(User)
    if username:
        user = users_query.filter_by(username=username).first()
        if not user:
            return {"message": "User with such id does not exist"}, 404
        return user.to_dict(), 200

    users_pagination = users_query.paginate(page=page, per_page=page_size)
    return {
        "result": [user.to_dict() for user in users_pagination.items],
        "page": users_pagination.page,
        "pages": users_pagination.pages,
        "total": users_pagination.total,
        "has_next": users_pagination.has_next,
        "has_prev": users_pagination.has_prev
    }


@bp.route("", methods=["PUT"])
@with_auth
def update_user(current_user: User):
    user_id = request.json.get("user_id")
    username = request.json.get("username")
    password = request.json.get("password")

    role = request.json.get("role")
    if role not in current_user.cached_roles:
        return {"message": f"Role '{role} does not exist"}, 404
    if role is not None and user_id is None:
        return {"message": "You cannot change your role"}, 403

    if current_user.role_id != current_app.cached_roles["admin"].id and user_id is not None:
        return {"message": "You cannot change other users` data"}, 403

    if user_id is not None:
        user_to_change = User.query.filter_by(id=user_id).first()
        if not user_to_change:
            return {"message": "User with such id does not exist"}, 404
    else:
        user_to_change = current_user

    if username:
        user_to_change.username = username
    if password:
        user_to_change.password = password
    if role:
        user_to_change.role_id = current_app.cached_roles[role].id
    db.session.commit()
    return {"message": "Changed user successfully"}, 200


@bp.route("", methods=["DELETE"])
@with_auth
def delete_user(current_user: User):
    user_id = request.json.get("user_id")

    if current_user.role_id != current_app.cached_roles["admin"].id and user_id is not None:
        return {"message": "You cannot delete other users"}, 403

    if user_id is not None:
        user_to_delete = User.query.filter_by(id=user_id).first()
        if not user_to_delete:
            return {"message": "User with such id does not exist"}, 404
    else:
        user_to_delete = current_user

    db.session.delete(user_to_delete)
    db.session.commit()
    return {"message": "User deleted successfully"}, 200
