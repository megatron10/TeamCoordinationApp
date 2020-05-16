# authentication
import json
import random
import string
import asyncio
import websockets

SID_LEN = 20

import sqlite3
import time

def register_sid(sid, username):
    expiry = time.time() + (24 * 60 * 60)
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("""INSERT INTO active VALUES (:uid, :sid, :expiry)""", {'uid':username, 'sid': sid, 'expiry':expiry})
    conn.commit()
    conn.close()


def get_random_sid():
    sid = ''.join(random.choice(string.ascii_letters) for i in range(101))
    return sid


def check_db(username, password):
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE username=:name AND transformedpass=:pass""", {'name':username, 'pass': password})
    count = len(c.fetchall())
    conn.close()
    if count >= 0:
        return True
    else:
        return False

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
