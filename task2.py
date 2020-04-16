import json
import asyncio
import websockets
from utils import check_valid_sid


async def communicate(websocket, path):
    # await register(websocket) . update local variables new connection established.

    try:
        async for message in websocket:
            data = json.loads(message)
            tosend = {"a": "b"}
            tosend = json.dumps(tosend)
            await websocket.send(tosend)

    finally:
        pass
        # await unregister(websocket). update local variables, connection broken.


def main(port=9002):
    start_server = websockets.serve(communicate, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
