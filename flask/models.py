from pydantic import BaseModel
from typing import Optional


class ProductCategoryImage(BaseModel):
    """Class for checking input data."""

    id: int
    source_to_img: str
    name: str
    price: Optional[float]
    description: Optional[str]
    featured_products: Optional[bool]
    featured_categories: Optional[bool]
