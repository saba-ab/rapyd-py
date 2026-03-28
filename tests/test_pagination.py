"""Tests for pagination helper."""

from unittest.mock import AsyncMock

from rapyd.models.payment import Payment
from rapyd.pagination import paginate


async def test_paginate_iterates_three_pages():
    """paginate() should iterate across 3 pages and yield all items."""
    page1 = [Payment(id="p1"), Payment(id="p2")]
    page2 = [Payment(id="p3"), Payment(id="p4")]
    page3 = [Payment(id="p5")]  # partial page → signals end

    mock_list = AsyncMock(side_effect=[page1, page2, page3])

    items = []
    async for item in paginate(mock_list, limit=2):
        items.append(item)

    assert len(items) == 5
    assert [i.id for i in items] == ["p1", "p2", "p3", "p4", "p5"]
    assert mock_list.call_count == 3


async def test_paginate_empty_first_page():
    """paginate() should stop immediately on empty first page."""
    mock_list = AsyncMock(return_value=[])

    items = []
    async for item in paginate(mock_list, limit=10):
        items.append(item)

    assert len(items) == 0
    assert mock_list.call_count == 1
