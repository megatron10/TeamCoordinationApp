import json
import asyncio
import websockets
from utils import check_valid_sid
import sqlite3
# channel list endpoint


def get_list_of_channels(uid):
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("""SELECT channelname FROM members WHERE username=:name""", {'name':uid})
    channel_list = [i[0] for i in c.fetchall()]
    conn.commit()
    conn.close()
    return channel_list



async def communicate(websocket, path):
    #  await register(websocket).
    #  update local variables new connection established.
    try:
        async for message in websocket:
            data = json.loads(message)
            is_valid_user = check_valid_sid(data['uid'], data['sid'])
            if not is_valid_user:
                status = 0
                channel_list = []
            else:
                status = 1
                channel_list = get_list_of_channels(data['uid'])
            tosend = {'status': status, "list": channel_list}
            tosend = json.dumps(tosend)
            await websocket.send(tosend)
    finally:
        pass
        # await unregister(websocket).
        # update local variables, connection broken.


def main(port=9005, url="localhost"):
    start_server = websockets.serve(communicate, url, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
