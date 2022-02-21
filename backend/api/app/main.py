from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.v1.router import router
from app.core.config import settings
from app.services.models.ingredient import IngredientExtractor


def get_app():
    """Generate instance of FastAPI app"""

    app = FastAPI(
        title=settings.title,
        description=settings.description,
        debug=settings.debug,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    app.include_router(router, prefix=settings.api_version)
    app.state.ingredient_model = IngredientExtractor()
    add_pagination(app)

    return app


app = get_app()
