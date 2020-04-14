import asyncio
import json
import websockets


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

def main():
    start_server = websockets.serve(communicate, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()