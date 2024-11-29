from .paths import spec as path_spec
from .components import spec as components_spec

spec = {
    "info": {
        "title": "Article API",
        "description": "API for managing articles",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "paths": {
        **path_spec
    },
    "components": {
        **components_spec
    },
    "security": [
        {
            "bearerAuth": []
        },
    ]
}
