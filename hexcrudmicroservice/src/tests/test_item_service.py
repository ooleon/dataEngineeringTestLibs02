import pytest
from unittest.mock import AsyncMock
from application.item_service import ItemService
from domain.entities import Item

@pytest.mark.asyncio
async def test_create_item_logs_and_persists():
    mock_repo = AsyncMock()
    mock_logger = AsyncMock()
    service = ItemService(repo=mock_repo, logger=mock_logger)
    item = Item(id="1", name="test", value="data")
    mock_repo.save.return_value = item

    result = await service.create(item)
    mock_repo.save.assert_awaited_once_with(item)
    mock_logger.info.assert_awaited_once_with("item_created", item_id="1", name="test")
    assert result == item

@pytest.mark.asyncio
async def test_get_nonexistent_returns_none():
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None
    service = ItemService(repo=mock_repo, logger=AsyncMock())
    assert await service.get("999") is None
