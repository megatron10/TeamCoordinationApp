import asyncio
import json
import websockets
import time
import random

USERS = set()
UID_to_USER = {}
val = 0

def get_msg(data):
    return json.dumps({'from_uid': data['uid'], "message": data['message'], "channel": data['channel']})

async def check_valid_sid(uid, sid):
    await asyncio.sleep(0.5)
    #await query the db
    # return sid > 0 and uid not in ['superman', 'batman', 'spiderman'] # just to test if the error handling works in case of invalid sid/uid
    return True

async def send_message_to_channel(data):
    await asyncio.sleep(0.5)
    #ls = await query the db for list of online UIDs for the channel
    ls = ['sahil', 'dhanno', 'anjani']
    message = get_msg(data)
    sender = data['uid']
    
    if data['action'] == 'connect':
        await UID_to_USER[sender].send(message)
        return 0

    for uid in ls:
        if uid in UID_to_USER and UID_to_USER[uid] not in USERS:
            UID_to_USER.pop(uid, 'uid not found')

    print(data['message'])

    to = [uid for uid in ls if uid != sender and UID_to_USER[uid] in USERS]
    if len(to) > 0: # asyncio.wait doesn't accept an empty. use list len(to) > 0 and 
        await asyncio.wait([UID_to_USER[uid].send(message) for uid in to])
    return 0

async def is_valid_send_request(uid, channel):
    await asyncio.sleep(0.5)
    #return await db query, is user uid allowed to use channel
    return True

#this is executed when the user first connects its web socket
def register(websocket):
    USERS.add(websocket)

def unregister(websocket):
    USERS.remove(websocket)

'''
To the client, just populate uid, sid, channel, action and message in each request.
The first message must have action field set to connect. All fields are at all times mandatory. Tho the values in these fields may not matter.
For example in the connect action (i.e. first interaction)
On successfully connecting the client will get a response message.
'''
async def communicate(websocket, path):
    register(websocket)
    
    try:
        async for message in websocket:
            data = json.loads(message)
            #first message
            if not await check_valid_sid(data['uid'], data['sid']):
                print('problem')
                await websocket.close()
                break
            else:
                UID_to_USER[data['uid']] = websocket
            
            is_cool = True
            if data['action'] != 'connect': # It can be 'send'
                is_cool = await is_valid_send_request(data['uid'], data['channel'])
            
            # print(is_cool)
            if is_cool:
                await send_message_to_channel(data)
            else:
                await websocket.send(json.dumps({"message": "invalid request"}))
    
    finally:
        unregister(websocket)

def main():
    start_server = websockets.serve(communicate, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()