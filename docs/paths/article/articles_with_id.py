spec = {
    "get": {
        "summary": "Get article by id",
        "description": "Get article with specified id.",
        "tags": [
            "Articles"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "article_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the article"
            }
        ],
        "responses": {
            "200": {
                "description": "Successful request. Article retrieved",
                "content": {
                    "application/json": {
                        "example": {
                            "content": "This is a guide on using SQLAlchemy in Python projects.",
                            "id": 1,
                            "title": "How to use SQLAlchemy",
                            "user_id": 2
                        }
                    }
                }
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "404": {
                "$ref": "#/components/responses/Article404"
            }
        }
    },
    "put": {
        "summary": "Update article",
        "tags": [
            "Articles"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "article_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the article"
            }
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string"
                            },
                            "content": {
                                "type": "string"
                            }
                        },
                        "example": {
                            "title": "New Title",
                            "content": "New Content",
                        }
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Successful update",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Article successfully updated"
                        }
                    }
                }
            },
            "400": {
                "$ref": "#/components/responses/BadValues"
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "403": {
                "description": "Insufficient rights",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "You cannot change this article"
                        }
                    }
                }
            },
            "404": {
                "$ref": "#/components/responses/Article404"
            }
        }
    },
    "delete": {
        "summary": "Delete article",
        "tags": [
            "Articles"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "article_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the article"
            }
        ],
        "responses": {
            "200": {
                "description": "Successful deletion",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Article successfully deleted"
                        }
                    }
                }
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "403": {
                "description": "Insufficient rights",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "You cannot delete this article"
                        }
                    }
                }
            },
            "404": {
                "$ref": "#/components/responses/Article404"
            }
        }
    }
}
