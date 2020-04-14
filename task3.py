import asyncio
import json
import websockets


async def communicate(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)
    tosend = {"a": "b"}
    tosend = json.dumps(tosend)
    await websocket.send(tosend)


def main():
    start_server = websockets.serve(communicate, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
