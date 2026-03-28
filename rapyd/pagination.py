"""Async pagination helper for Rapyd list endpoints."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any, Callable, Coroutine


async def paginate(
    resource_method: Callable[..., Coroutine[Any, Any, list[Any]]],
    **kwargs: Any,
) -> AsyncGenerator[Any, None]:
    """Async generator that auto-paginates a list endpoint.

    Usage::

        async for payment in paginate(rapyd.payments().list, limit=50):
            print(payment.id)

    Fetches pages sequentially using ``starting_after`` cursor until
    no more results are returned.
    """
    limit = kwargs.pop("limit", 10)
    while True:
        page = await resource_method(limit=limit, **kwargs)
        if not page:
            break
        for item in page:
            yield item
        if len(page) < limit:
            break
        # Use the last item's id as the cursor for the next page
        kwargs["starting_after"] = page[-1].id
