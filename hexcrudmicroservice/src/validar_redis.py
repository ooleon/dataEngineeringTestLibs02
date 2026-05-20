import redis
import redis.asyncio as aioredis

print(f"redis-py versión: {redis.__version__}")  # Debe ser >= 4.2.0 (actualmente 5.x)
print(f"Módulo asíncrono disponible: {hasattr(redis, 'asyncio')}")  # True
# Conexión (compatible con Redis, Valkey y Dragonfly)
client = aioredis.from_url(
    "redis://localhost:6379",
    decode_responses=True,  # Devuelve strings en lugar de bytes
    socket_timeout=2.0
)

async def example():
    await client.set("user:1", '{"name":"admin"}')
    data = await client.get("user:1")
    print(data)
    await client.close()
