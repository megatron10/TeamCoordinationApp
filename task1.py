# import random
# import time
import json
import time
import asyncio
import websockets
from utils import check_valid_sid
import sqlite3


def changedate(num):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(num)))


async def get_messages_from_channel(uid, sid, channel):
    # await asyncio.sleep(sid)  # waited on sid to test concurrency
    # await query the db
    conn = sqlite3.connect("/tmp/data.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM " + channel + " ORDER BY time DESC LIMIT 10;"
    )
    ls = c.fetchall()
    ls = [(i, j, changedate(k)) for (i, j, k) in ls]
    conn.commit()
    conn.close()
    return ls


async def communicate(websocket, path):
    # await register(websocket) .
    # update local variables new connection established.
    try:
        async for message in websocket:
            data = json.loads(message)

            # print('sid ', data['sid'], 'asked for messages on channel',
            # data['channel'])
            var = check_valid_sid(data["uid"], data["sid"])

            # print(var)
            if not var:
                await websocket.close()
                break

            # print(data['sid'], ' approved for messages')
            # print(f"started at {time.strftime('%X')}")

            msgs = await get_messages_from_channel(
                data["uid"], data["sid"], data["channel"]
            )

            # print(data['sid'], 'got its messages')
            # print(f"ended at {time.strftime('%X')}")

            tosend = {"ret": msgs}
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


if __name__ == "__main__":
    main()
