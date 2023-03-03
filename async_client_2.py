import asyncio
import aiofiles

from loguru import logger

logger.add("info.log", format="{time} {level} {message}", level="INFO")

async def tcp_client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8886)

    async with aiofiles.open('data.json', mode='r') as f:
        message = await f.read()

    logger.info(f"Send: {message}")
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    logger.info(f'Received: {data.decode()!r}')

    logger.info('Close the connection')
    writer.close()
    await writer.wait_closed()


asyncio.run(tcp_client())