from elasticsearch import AsyncElasticsearch
import datetime

class ElasticsearchLogger:
    def __init__(self, hosts: list[str], index_prefix: str = "app-logs"):
        self._client = AsyncElasticsearch(hosts, request_timeout=3)
        self._index_prefix = index_prefix

    async def _push(self, level: str, message: str, **ctx):
        index = f"{self._index_prefix}-{datetime.date.today().isoformat()}"
        await self._client.index(
            index=index,
            document={"level": level, "msg": message, "ctx": ctx, "@timestamp": datetime.datetime.now(datetime.UTC).isoformat()}
        )

    async def info(self, message: str, **context):
        await self._push("INFO", message, **context)
    async def error(self, message: str, **context):
        await self._push("ERROR", message, **context)
