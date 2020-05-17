# import time
# import random
import json
import asyncio
import websockets
from utils import check_valid_sid
import sqlite3

USER_to_UID = {}
UID_to_USER = {}


def inform_status_msg(uid, status):
    return json.dumps({"from_uid": uid, "message": status})


async def send_online_contacts_list(websocket, uid):
    # await query db for online contacts of 'uid'
    conn = sqlite3.connect("/tmp/data.db")
    c = conn.cursor()
    c.execute("""SELECT * FROM online""")
    ls = [i[0] for i in c.fetchall()]
    conn.close()
    await websocket.send(json.dumps({"action": "list", "message": repr(ls)}))


async def inform_contacts(uid, status):
    # await query db for online contacts of 'uid'
    conn = sqlite3.connect("/tmp/data.db")
    c = conn.cursor()
    c.execute("""SELECT * FROM online""")
    ls = [i[0] for i in c.fetchall()]
    conn.close()
    # ls = ['sahil', 'dhanno', 'anjani']
    to = [contact_id for contact_id in ls if contact_id in UID_to_USER]
    if len(to) > 0:  # asyncio.wait doesn't accept an empty.
        await asyncio.wait(
            [
                UID_to_USER[contact_id].send(inform_status_msg(uid, status))
                for contact_id in to
            ]
        )
    return 0


# this is executed when the user first connects its web socket
async def register(websocket, data):
    UID_to_USER[data["uid"]] = websocket
    USER_to_UID[websocket] = data["uid"]
    # await update online status in DB for user 'uid'
    await send_online_contacts_list(websocket, data["uid"])
    await inform_contacts(data["uid"], "online")
    conn = sqlite3.connect("/tmp/data.db")
    c = conn.cursor()
    c.execute("""INSERT INTO online VALUES (:name)""", {"name": data['uid']})
    conn.commit()
    conn.close()


async def unregister(websocket):
    if websocket in USER_to_UID:
        user = USER_to_UID[websocket]
        UID_to_USER.pop(user, "user not found")
        USER_to_UID.pop(websocket)
        # await update status of 'user' to offline in db
        await inform_contacts(user, "offline")
        conn = sqlite3.connect("/tmp/data.db")
        c = conn.cursor()
        c.execute("""DELETE FROM online WHERE uid=:name""", {"name": user})
        conn.commit()
        conn.close()
    return 0


async def communicate(websocket, path):
    """
    To the client, just populate uid, sid, action and request in each
    request. The first message must have action field set to connect. All
    fields are at all times mandatory.
    On connecting the server will send the client a list of online users in
    the org. The server shall send messages to inform about any change in
    online status of users.
    """

    try:
        async for message in websocket:
            data = json.loads(message)
            # invalid session id
            if not check_valid_sid(data["uid"], data["sid"]):
                print("problem")
                await websocket.close()
                break
            # connect and get list of online contacts, after this client will
            # be updated whenever a contact changes status
            elif data["action"] == "connect":
                await register(websocket, data)
            # invalid request, this process does nothing else
            else:
                await websocket.send(json.dumps({"message": "invalid request"}))

    finally:
        await unregister(websocket)


def main(port=9002):
    start_server = websockets.serve(communicate, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
