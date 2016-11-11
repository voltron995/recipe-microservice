class RecipeSchema:
    post = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            'description': {'type': "string"},
            "img_path": {"type": "string"},
            "ingredients": {"type": "object"},
            "categories": {"type": "array"}
        },
        "required": ["name", "ingredients", "categories"],
    }
    put = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "img_path": {"type": "string"},
            "ingredients": {"type": "object"},
            "categories": {"type": "array"}
        },
        "required": ["id"],
    }
    delete = {
        "type": "object",
        "properties": {
            "id": {"type": "number"}
        },
        "required": ["id"]
    }

class CategorySchema:
    post = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    put = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"}
        },
        "required": ["id"],
    }
    delete = {
        "type": "object",
        "properties": {
            "id": {"type": "number"}
        },
        "required": ["id"]
    }