import pytest
from testcontainers.redis import RedisContainer
from testcontainers.kafka import KafkaContainer
from testcontainers.elasticsearch import ElasticSearchContainer
from testcontainers.core.waiting_utils import wait_for_logs
from domain.entities import Item
from application.item_service import ItemService
from infrastructure.cache.valkey_adapter import ValkeyItemRepository
from infrastructure.logging.console_handler import ConsoleLogger
from unittest.mock import AsyncMock


@pytest.fixture(scope="session")
def valkey_container():
    with RedisContainer("valkey/valkey:8-alpine") as redis:
        # wait_for_logs is implicit in testcontainers redis module
        yield f"redis://localhost:{redis.port}"


@pytest.fixture
async def service(valkey_container):
    repo = ValkeyItemRepository(url=valkey_container, db=0)
    logger = ConsoleLogger()  # Console para evitar dependencia de brokers en unit tests
    return ItemService(repo=repo, logger=logger)


@pytest.mark.asyncio
async def test_crud_lifecycle(service):
    item = Item(id="test-1", name="integration", value="payload")

    # Create
    created = await service.create(item)
    assert created.id == "test-1"

    # Read
    fetched = await service.get("test-1")
    assert fetched is not None and fetched.name == "integration"

    # List
    items = await service.list_all()
    assert any(i.id == "test-1" for i in items)

    # Delete
    deleted = await service.delete("test-1")
    assert deleted is True
    assert await service.get("test-1") is None