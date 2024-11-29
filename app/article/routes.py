from flask import request, current_app
from sqlalchemy import or_

from app import db
from app.article import bp
from app.article.models import Article
from app.users.models import User
from app.utils import with_auth, with_validation


@bp.route("", methods=["GET"])
@with_auth
def get_articles(user: User):
    search_query = request.args.get("search_query")
    user_id = request.args.get("user_id")

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        return {"message": "Page number must be int value!"}, 400

    page_size = current_app.config["PAGE_SIZE"]

    articles_query = db.session.query(Article)
    if user_id:
        articles_query = articles_query.filter_by(user_id=user_id)
    if search_query:
        articles_query = articles_query.where(or_(
            Article.title.match(search_query),
            Article.content.match(search_query)
        ))

    articles_pagination = articles_query.paginate(page=page, per_page=page_size)
    return {
        "result": [article.to_dict() for article in articles_pagination.items],
        "page": articles_pagination.page,
        "pages": articles_pagination.pages,
        "total": articles_pagination.total,
        "has_next": articles_pagination.has_next,
        "has_prev": articles_pagination.has_prev
    }


@bp.route("/<int:article_id>", methods=["GET"])
@with_auth
def get_article_by_id(user: User, article_id: int):
    article = Article.query.filter_by(id=int(article_id)).first()
    if not article:
        return {"message": "Article with such id does not exist"}, 404
    return article.to_dict(), 200


@bp.route("", methods=["POST"])
@with_auth
@with_validation({"title": str, "content": str})
def add_article(user: User):
    title = request.json["title"]
    content = request.json["content"]

    article = Article(title=title, content=content, user=user)
    db.session.add(article)
    db.session.commit()
    return article.to_dict(), 201


@bp.route("/<int:article_id>", methods=["PUT"])
@with_auth
def update_article(user: User, article_id: int):
    title = request.json.get("title")
    content = request.json.get("content")

    article = Article.query.filter_by(id=article_id).first()
    if not article:
        return {"message": "Article with such id does not exist"}, 404

    allowed_roles = (current_app.cached_roles["admin"].id, current_app.cached_roles["editor"].id)
    if article.user != user and user.role_id not in allowed_roles:
        return {"message": "You cannot change this article"}, 403

    if title:
        article.title = title
    if content:
        article.content = content
    db.session.commit()
    return {"message": "Article successfully updated"}, 200


@bp.route("/<int:article_id>", methods=["DELETE"])
@with_auth
def delete_article(user: User, article_id: int):
    article = Article.query.filter_by(id=article_id).first()
    if not article:
        return {"message": "Article with such id does not exist"}, 404

    if article.user != user and user.role_id != current_app.cached_roles["admin"].id:
        return {"message": "You cannot delete this article"}, 403

    db.session.delete(article)
    db.session.commit()
    return {"message": "Article successfully deleted"}, 200
