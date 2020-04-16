import json
import asyncio
import websockets

# channel list endpoint


def check_valid_sid(uid, sid):
    #  TODO
    return True


def get_list_of_channels(uid):
    #  TODO get channel list for user uid
    channel_list = [f"#channel-{i}" for i in range(10)]
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


def main(port=9005):
    start_server = websockets.serve(communicate, "localhost", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
