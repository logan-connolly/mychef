from typing import TypedDict


class Source(TypedDict):
    """Schema that matches MyChef API definition for `Source`"""

    name: str
    url: str


class Recipe(TypedDict):
    """Schema that matches MyChef API definition for `Recipe`"""

    name: str
    image: str
    ingredients: str
    source_id: int
    url: str
