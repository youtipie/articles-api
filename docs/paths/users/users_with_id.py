spec = {
    "get": {
        "summary": "Get user by id",
        "description": "Get user with specified id.",
        "tags": [
            "Users"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "user_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the user"
            }
        ],
        "responses": {
            "200": {
                "description": "Successful request. User retrieved",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "role_id": 1,
                            "username": "admin"
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
    "put": {
        "summary": "Update user",
        "tags": [
            "Users"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "user_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the user"
            }
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string"
                            },
                            "password": {
                                "type": "string"
                            },
                            "role": {
                                "type": "string"
                            }
                        },
                        "example": {
                            "username": "New username",
                            "password": "NewSecurePassword12345",
                            "role": "editor"
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
                            "message": "Changed user successfully"
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
                            "message": "You cannot change other users` data"
                        }
                    }
                }
            },
            "404": {
                "$ref": "#/components/responses/User404"
            }
        }
    },
    "delete": {
        "summary": "Delete user",
        "tags": [
            "Users"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "user_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the user"
            }
        ],
        "responses": {
            "200": {
                "description": "Successful deletion",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "User deleted successfully"
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
                            "message": "You cannot delete other users"
                        }
                    }
                }
            },
            "404": {
                "$ref": "#/components/responses/User404"
            }
        }
    }
}
