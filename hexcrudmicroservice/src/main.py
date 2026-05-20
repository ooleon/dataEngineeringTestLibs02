from fastapi import FastAPI, HTTPException
import flet as ft
from pydantic_settings import BaseSettings
from application.item_service import ItemService
from domain.entities import Item
import os

__title__ = "Hexagonal CRUD Microservice"

class AppConfig(BaseSettings):
    cache_backend: str = "redis"
    cache_url: str = "redis://localhost:6379"
    log_backend: str = "console"
    kafka_brokers: str = "localhost:9092"
    kafka_topic: str = "app-logs"
    es_hosts: str = "http://localhost:9200"
    model_config = {"env_file": ".env", "extra": "ignore"}

cfg = AppConfig()

def get_repository():
    match cfg.cache_backend:
        case "redis":
            from infrastructure.cache.redis_adapter import RedisItemRepository
            return RedisItemRepository(url=cfg.cache_url)
        case "valkey":
            from infrastructure.cache.valkey_adapter import ValkeyItemRepository
            return ValkeyItemRepository(url=cfg.cache_url)
        case "dragonfly":
            from infrastructure.cache.dragonfly_adapter import DragonflyItemRepository
            return DragonflyItemRepository(url=cfg.cache_url)
        case _:
            raise ValueError(f"Unsupported cache_backend: {cfg.cache_backend}")

def get_logger():
    match cfg.log_backend:
        case "console":
            from infrastructure.logging.console_handler import ConsoleLogger
            return ConsoleLogger()
        case "kafka":
            from infrastructure.logging.kafka_handler import KafkaLogger
            return KafkaLogger(brokers=cfg.kafka_brokers.split(","), topic=cfg.kafka_topic)
        case "elasticsearch":
            from infrastructure.logging.elasticsearch_handler import ElasticsearchLogger
            return ElasticsearchLogger(hosts=cfg.es_hosts.split(","))
        case _:
            raise ValueError(f"Unsupported log_backend: {cfg.log_backend}")

repo = get_repository()
logger = get_logger()
service = ItemService(repo, logger)

#app = FastAPI(title="Hexagonal CRUD Microservice")
app = FastAPI(title=__title__)

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    return await service.create(item)

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    result = await service.get(item_id)
    if not result:
        raise HTTPException(404, "Item not found")
    return result

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if not await service.delete(item_id):
        raise HTTPException(404, "Item not found")
    return {"status": "deleted"}

@app.get("/items", response_model=list[Item])
async def list_items():
    return await service.list_all()



async def main(page: ft.Page):
    page.title = __title__
    page.add(ft.Text("paso"))

if __name__ == '__main__':
    ft.run(main=main)
