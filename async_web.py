import asyncio
from loguru import logger
import ast

logger.add("info.log", format="{time} {level} {message}", level="INFO")

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    logger.info(f"Connected by {addr}")
    request = (await reader.read(1024)).decode("utf-8")

    d = ast.literal_eval(request)

    if isinstance(d, dict):
        if d.get("+"):
            lst = d.get("+")
            if all((len(d)==1, len(lst)==2, list(d.keys())==['+'], all(isinstance(x, int) for x in lst))):
                response = str(sum(lst))
                writer.write(response.encode("utf-8"))
            else:
                writer.write("wrong data".encode("utf-8"))
        else:
            writer.write("There is no such operations ".encode("utf-8"))
    else:
        writer.write("This is not object".encode("utf-8"))

    await writer.drain()
    writer.close()
    logger.info(f"Disconnected by {addr}")

async def main(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    async with server:
        await server.serve_forever()

HOST, PORT = "localhost", 8886

if __name__ == "__main__":
    asyncio.run(main(HOST, PORT))