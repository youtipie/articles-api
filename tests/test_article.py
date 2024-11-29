import pytest
from unittest.mock import patch

from app import db
from app.article.models import Article

ARTICLES_AMOUNT = 10


@pytest.fixture
def generate_articles(app, with_user):
    user_id, _, _ = with_user
    with app.app_context():
        for i in range(ARTICLES_AMOUNT):
            title = f"title{i}"
            content = f"content{i}"

            user = Article(title=title, content=content, user_id=user_id)
            db.session.add(user)
        db.session.commit()


def test_get_all_articles(app, client, access_headers, generate_articles):
    response = client.get("/article", headers=access_headers)
    data = response.json
    assert response.status_code == 200
    assert data["has_prev"] == False
    assert data["has_next"] == True
    assert data["page"] == 1
    assert data["pages"] == 2
    assert len(data["result"]) == app.config["PAGE_SIZE"]
    assert data["total"] == ARTICLES_AMOUNT


def test_get_all_articles_using_page(app, client, access_headers, generate_articles):
    response = client.get("/article?page=2", headers=access_headers)
    data = response.json
    assert response.status_code == 200
    assert data["has_prev"] == True
    assert data["has_next"] == False
    assert data["page"] == 2
    assert data["pages"] == 2
    assert len(data["result"]) == app.config["PAGE_SIZE"]
    assert data["total"] == ARTICLES_AMOUNT


def test_get_article_by_username(client, access_headers, generate_articles):
    with patch("sqlalchemy.orm.attributes.InstrumentedAttribute.match") as mock_match:
        mock_match.return_value = Article.title.like("%title1%")
        response = client.get("/article?search_query=title1", headers=access_headers)
        data = response.json
        user = data["result"][0]
        assert response.status_code == 200
        assert data["has_prev"] == False
        assert data["has_next"] == False
        assert data["page"] == 1
        assert data["pages"] == 1
        assert len(data["result"]) == 1
        assert data["total"] == 1
        assert user["title"] == "title1"


def test_get_article_by_id(client, access_headers, generate_articles):
    response = client.get("/article/1", headers=access_headers)
    article = response.json
    assert response.status_code == 200
    assert article["title"] == "title0"


def test_add_article(client, access_headers):
    title = "New article"
    content = "Content"
    response = client.post("/article", headers=access_headers, json={"title": title, "content": content})
    assert response.status_code == 201
    assert response.json["title"] == title
    assert response.json["content"] == content
    article = Article.query.filter_by(title=title).first()
    assert article.id == response.json["id"]
    assert article.title == title
    assert article.content == content


def test_update_article(app, client, access_headers, generate_articles):
    with app.app_context():
        article_to_update = Article.query.filter_by(id=2).first()

    new_title = "Updated title"
    new_content = "Updated content"

    response = client.put(f"/article/{article_to_update.id}", headers=access_headers, json={
        "title": new_title,
        "content": new_content,
    })
    data = response.json
    assert response.status_code == 200
    assert data["message"] == "Article successfully updated"

    with app.app_context():
        article = Article.query.filter_by(id=article_to_update.id).first()
        assert article.title == new_title
        assert article.content == new_content


def test_delete_article(app, client, access_headers, generate_articles):
    response = client.delete("/article/2", headers=access_headers)
    assert response.status_code == 200
    assert response.json["message"] == "Article successfully deleted"
    with app.app_context():
        article = Article.query.filter_by(id=2).first()
        assert article is None
