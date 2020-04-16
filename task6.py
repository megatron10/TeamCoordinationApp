# authentication
import json
import random
import string
import asyncio
import websockets

SID_LEN = 20


def register_sid(sid, username):
    # TODO store sid to db
    pass


def get_random_sid():
    sid = ''.join(random.choice(string.ascii_letters) for i in range(101))
    return sid


def check_db(username, password):
    #  TODO
    return True


def check_auth(data):
    status = 0
    sid = ""
    try:
        username = data['username']
        password = data['transformed_password']
        if check_db(username, password):
            status = 1
            sid = get_random_sid()
            register_sid(sid, username)
        else:
            status = 0
            sid = ""
    except Exception:
        status = 0
        sid = ""
    finally:
        return status, sid


async def communicate(websocket, path):
    # here we can register websocket
    try:
        async for message in websocket:
            data = json.loads(message)
            status, sid = check_auth(data)
            if status == 1:
                pass
                # we can register here if needed
                # register_online_user(data['username'], websocket)
            tosend = {"status": status, 'sid': sid}
            tosend = json.dumps(tosend)
            await websocket.send(tosend)
    finally:
        pass
        # await unregister(websocket).
        # update local variables, connection broken.


def main(port=9006):
    start_server = websockets.serve(communicate, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
