spec = {
    "UnauthorizedError": {
        "description": "No token provided",
        "content": {
            "application/json": {
                "example": {
                    "msg": "Missing Authorization Header."
                }
            }
        }
    },
    "User404": {
        "description": "User does not exist",
        "content": {
            "application/json": {
                "example": {
                    "message": "User with such id does not exist."
                }
            }
        }
    },
    "Article404": {
        "description": "No article found",
        "content": {
            "application/json": {
                "example": {
                    "message": "Article with such id does not exist"
                }
            }
        }
    },
    "BadValues": {
        "description": "Missing required fields in request body",
        "content": {
            "application/json": {
                "example": {
                    "message": "Request body must be JSON and contain username and password"
                }
            }
        }
    }
}
