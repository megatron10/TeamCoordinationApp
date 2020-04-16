# import random
# import time
import json
import asyncio
import websockets
from utils import check_valid_sid


async def get_messages_from_channel(uid, sid, channel):
    await asyncio.sleep(sid)  # waited on sid to test concurrency
    # await query the db
    ls = ['1', '2', 'cha', 'cha', 'cha']
    ls.append(channel)
    return ls


async def communicate(websocket, path):
    # await register(websocket) .
    # update local variables new connection established.
    try:
        async for message in websocket:
            data = json.loads(message)

            # print('sid ', data['sid'], 'asked for messages on channel', data['channel'])
            var = check_valid_sid(data['uid'], data['sid'])

            # print(var)
            if not var:
                await websocket.close()
                break

            # print(data['sid'], ' approved for messages')
            # print(f"started at {time.strftime('%X')}")

            msgs = await get_messages_from_channel(data['uid'], data['sid'], data['channel'])

            # print(data['sid'], 'got its messages')
            # print(f"ended at {time.strftime('%X')}")

            tosend = {"ret": repr(msgs)}
            tosend = json.dumps(tosend)
            await websocket.send(tosend)

    finally:
        pass
        # await unregister(websocket).
        # update local variables, connection broken.


def main(port=9001):
    start_server = websockets.serve(communicate, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
