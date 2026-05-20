import structlog
import asyncio

structlog.configure(processors=[structlog.processors.JSONRenderer()])

class ConsoleLogger:
    async def info(self, message: str, **context):
        await asyncio.to_thread(structlog.get_logger().info, message, **context)
    async def error(self, message: str, **context):
        await asyncio.to_thread(structlog.get_logger().error, message, **context)
