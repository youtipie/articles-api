spec = {
    "get": {
        "summary": "Get users roles",
        "description": "Get all available roles",
        "tags": [
            "Users"
        ],
        "security": [],
        "responses": {
            "200": {
                "description": "Successful request. The list of all available roles is retrieved",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "name": "Admin"
                            },
                            {
                                "id": 2,
                                "name": "Editor"
                            },
                            {
                                "id": 3,
                                "name": "Viewer"
                            }
                        ]
                    }
                }
            }
        }
    }
}
