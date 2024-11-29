spec = {
    "get": {
        "summary": "Get all users",
        "description": "Get and filter all users.",
        "tags": [
            "Users"
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
                "name": "username",
                "schema": {
                    "type": "string"
                },
                "required": False,
                "description": "Filter users by specified username."
            }
        ],
        "responses": {
            "200": {
                "description": "Successful request. The list of all users retrieved",
                "content": {
                    "application/json": {
                        "example": {
                            "has_next": False,
                            "has_prev": False,
                            "page": 1,
                            "pages": 1,
                            "result": [
                                {
                                    "id": 1,
                                    "role_id": 1,
                                    "username": "admin"
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
    }
}
