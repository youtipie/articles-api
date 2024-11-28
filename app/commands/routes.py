from flask import current_app
from sqlalchemy.exc import IntegrityError

from app import db
from app.article.models import Article
from app.commands import bp
from app.users.models import User


@bp.cli.command("create-user")
def create_user():
    while True:
        try:
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role name (admin, editor, viewer): ")
            if role not in current_app.cached_roles:
                print("Such role does not exist")
                continue
            user = User(username=username, password=password, role_id=current_app.cached_roles.get(role).id)
        except ValueError as e:
            print(str(e))
        except IntegrityError as e:
            print(str(e))
        else:
            db.session.add(user)
            db.session.commit()
            print(f"User '{username}' created successfully!")
            break


@bp.cli.command("prepopulate-db")
def prepopulate_db():
    admin_user = User(username="admin", password="Admin1234", role_id=current_app.cached_roles.get("admin").id)
    editor_user = User(username="editor", password="Editor1234", role_id=current_app.cached_roles.get("editor").id)
    viewer_user = User(username="viewer", password="Viewer1234", role_id=current_app.cached_roles.get("viewer").id)

    db.session.add_all([admin_user, editor_user, viewer_user])
    db.session.commit()

    article_1 = Article(
        title="How to use SQLAlchemy",
        content="This is a guide on using SQLAlchemy in Python projects.",
        user_id=editor_user.id
    )
    article_2 = Article(
        title="Flask for Beginners",
        content="Flask is a lightweight Python web framework.",
        user_id=editor_user.id
    )

    db.session.add_all([article_1, article_2])
    db.session.commit()

    print("Database has been populated with sample data.")
