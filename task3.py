# import time
# import random
import json
import asyncio
import websockets
from utils import check_valid_sid

USER_to_UID = {}
UID_to_USER = {}


def get_msg(data):
    return json.dumps({'from_uid': data['uid'], "message": data['message'], "channel": data['channel']})


async def send_message_to_channel(data):
    await asyncio.sleep(0.5)
    # ls = await query the db for list of online UIDs for the channel
    ls = ['sahil', 'dhanno', 'anjani']
    message = get_msg(data)
    sender = data['uid']

    to = [uid for uid in ls if uid != sender and uid in UID_to_USER]
    if len(to) > 0:  # asyncio.wait doesn't accept an empty. use list len(to) > 0 and
        await asyncio.wait([UID_to_USER[uid].send(message) for uid in to])
    return 0


async def is_valid_send_request(uid, channel):
    await asyncio.sleep(0.5)
    # return await db query, is user uid allowed to use channel
    return True

# this is executed when the user first connects and sends a 'connect' action message
async def register(websocket, uid, message):
    USER_to_UID[websocket] = uid
    UID_to_USER[uid] = websocket
    await websocket.send(message)

def unregister(websocket):
    if websocket in USER_to_UID:
        user = USER_to_UID[websocket]
        UID_to_USER.pop(user, 'user not found')
        USER_to_UID.pop(websocket)

async def communicate(websocket, path):
    '''
    To the client, just populate uid, sid, channel, action and message fields in each request.
    For first message use action = 'connect'
    To send messages use action = 'send'
    You will be notified of incoming messages from this websocket after you have connected.
    '''	

    try:
        async for message in websocket:
            data = json.loads(message)
            
            # invalid session id
            if not check_valid_sid(data['uid'], data['sid']):
                print('problem')
                await websocket.close()
                break
            
            # connect and get confirmation message echoed back. Can send messages after this and will receive messages for other users messages.
            elif data['action'] == 'connect':
                await register(websocket, data['uid'], message)

            # send a message
            elif data['action'] == 'send':
            	if await is_valid_send_request(data['uid'], data['channel']):
                	await send_message_to_channel(data)
            	else:
                	await websocket.send(json.dumps({"message": "invalid request, can't send message on this channel"}))
            
            # not a recognized action
            else:
            	await websocket.send(json.dumps({"message": "invalid action"}))
    
    finally:
        unregister(websocket)


def main(port=9003):
    start_server = websockets.serve(communicate, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
