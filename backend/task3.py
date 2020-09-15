# import time
# import random
import time
import json
import asyncio
import sqlite3
import websockets
from utils import check_valid_sid


USER_to_UID = {}
UID_to_USER = {}
online_uids = set()


def get_msg(data):
    return json.dumps(
        {
            "from_uid": data["uid"],
            "message": data["message"],
            "channel": data["channel"],
        }
    )


def get_users_in_channel(channel):
    conn = sqlite3.connect("/tmp/data.db")
    c = conn.cursor()
    c.execute("SELECT username FROM members WHERE channelname=:ch" "",
              {"ch": channel})
    ls = [i[0] for i in c.fetchall()]
    conn.commit()
    conn.close()
    return ls


async def send_message_to_users(data):
    # await asyncio.sleep(0.5)
    # ls = await query the db for list of online UIDs for the channel
    users_in_channel = set(get_users_in_channel(data["channel"]))
    onlines = users_in_channel.intersection(online_uids)

    message = get_msg(data)
    sender = data["uid"]

    to = [uid for uid in onlines if uid != sender and uid in UID_to_USER]
    if len(to) > 0:  # asyncio.wait doesn't accept an empty.
        await asyncio.wait([UID_to_USER[uid].send(message) for uid in to])
    return 0


def add_message_to_channel(uid, msg, channel):
    conn = sqlite3.connect("/tmp/data.db")
    c = conn.cursor()
    c.execute(
        f"INSERT INTO {channel} VALUES (:username, :msg, :time)",
        {"username": uid, "msg": msg, "time": time.time()},
    )
    conn.commit()
    conn.close()


def is_valid_send_request(uid, channel):
    conn = sqlite3.connect("/tmp/data.db")
    c = conn.cursor()
    c.execute(
        """ SELECT * FROM members
    WHERE username=:name AND channelname=:ch""",
        {"name": uid, "ch": channel},
    )
    count = len(c.fetchall())
    conn.close()
    if count >= 0:
        return True
    else:
        return False


# this is executed when the user first connects and sends a 'connect' action
# message
async def register(websocket, uid, message):
    USER_to_UID[websocket] = uid
    UID_to_USER[uid] = websocket
    online_uids.add(uid)
    await websocket.send(message)


def unregister(websocket):
    if websocket in USER_to_UID:
        user = USER_to_UID[websocket]
        UID_to_USER.pop(user, "user not found")
        USER_to_UID.pop(websocket)
        online_uids.remove(user)


async def communicate(websocket, path):
    """
    To the client, just populate uid, sid, channel, action and message fields
    in each request.
    For first message use action = 'connect'
    To send messages use action = 'send'
    You will be notified of incoming messages from this websocket after you 
    have connected.
    """

    try:
        async for message in websocket:
            data = json.loads(message)

            # invalid session id
            if not check_valid_sid(data["uid"], data["sid"]):
                print("problem")
                await websocket.close()
                break

            # connect and get confirmation message echoed back. Can send
            # messages after this and will receive messages for other users
            # messages.
            elif data["action"] == "connect":
                await register(websocket, data["uid"], message)

            # send a message
            elif data["action"] == "send":
                if is_valid_send_request(data["uid"], data["channel"]):
                    await send_message_to_users(data)
                    add_message_to_channel(
                        data["uid"], data["message"], data["channel"]
                    )
                else:
                    await websocket.send(json.dumps({"message": "invalid request"}))

            # not a recognized action
            else:
                await websocket.send(json.dumps({"message": "invalid action"}))

    finally:
        unregister(websocket)


def main(port=9003, url="localhost"):
    start_server = websockets.serve(communicate, url, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
