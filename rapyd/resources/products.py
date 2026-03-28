"""Products resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Product
from rapyd.resources.base import BaseResource


class ProductsResource(BaseResource):
    """Interact with the Rapyd Products API (``/v1/products``)."""

    async def create(self, **kwargs: Any) -> Product:
        """Create a product.

        Args:
            name: Product name.
            type: Product type ("service" or "good").

        Returns:
            Product object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/products", body=kwargs)
        return Product.model_validate(self._extract_data(resp))

    async def get(self, product_id: str) -> Product:
        """Retrieve a product by ID.

        Args:
            product_id: The product token.

        Returns:
            Product object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/products/{product_id}")
        return Product.model_validate(self._extract_data(resp))

    async def update(self, product_id: str, **kwargs: Any) -> Product:
        """Update a product.

        Args:
            product_id: The product token.
            name: Updated name.
            description: Updated description.

        Returns:
            Updated Product object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/products/{product_id}", body=kwargs)
        return Product.model_validate(self._extract_data(resp))

    async def delete(self, product_id: str) -> dict[str, Any]:
        """Delete a product.

        Args:
            product_id: The product token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/products/{product_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Product]:
        """List products with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Product objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/products", params=params)
        data = self._extract_data(resp)
        return [Product.model_validate(item) for item in (data or [])]
