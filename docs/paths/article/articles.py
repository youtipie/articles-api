spec = {
    "get": {
        "summary": "Get all articles",
        "description": "Get and filter all articles.",
        "tags": [
            "Articles"
        ],
        "parameters": [
            {
                "in": "query",
                "name": "page",
                "schema": {
                    "type": "integer"
                },
                "required": False,
                "description": "Pagination page. Defaults to 1 if no specified."
            },
            {
                "in": "query",
                "name": "search_query",
                "schema": {
                    "type": "string"
                },
                "required": False,
                "description": "Filter articles by specified string."
            },
            {
                "in": "query",
                "name": "user_id",
                "schema": {
                    "type": "integer"
                },
                "required": False,
                "description": "Filter articles by specified user."
            }
        ],
        "responses": {
            "200": {
                "description": "Successful request. The list of all articles retrieved",
                "content": {
                    "application/json": {
                        "example": {
                            "has_next": False,
                            "has_prev": False,
                            "page": 1,
                            "pages": 1,
                            "result": [
                                {
                                    "content": "This is a guide on using SQLAlchemy in Python projects.",
                                    "id": 1,
                                    "title": "How to use SQLAlchemy",
                                    "user_id": 2
                                },
                                {
                                    "content": "Flask is a lightweight Python web framework.",
                                    "id": 2,
                                    "title": "Flask for Beginners",
                                    "user_id": 2
                                }
                            ],
                            "total": 1
                        }
                    }
                }
            },
            "400": {
                "description": "Invalid page number",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Page number must be int value"
                        }
                    }
                }
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "404": {
                "$ref": "#/components/responses/User404"
            }
        }
    },
    "post": {
        "summary": "Add new article",
        "tags": [
            "Articles"
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
                            "title": "Title",
                            "content": "Content"
                        }
                    }
                }
            }
        },
        "responses": {
            "201": {
                "description": "Newly created article",
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
            "400": {
                "$ref": "#/components/responses/BadValues"
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "404": {
                "$ref": "#/components/responses/User404"
            }
        }
    }
}
