import json
import asyncio
import websockets

# person info endpoint


def check_valid_sid(uid, sid):
    #  TODO
    return True


def get_person_info(uid):
    #  TODO get person info
    info = {
        "username": "dhanno",
        "display-name": "Dhananjay Raut",
        "icon_link": ""
    }
    return info


async def communicate(websocket, path):
    #  await register(websocket).
    #  update local variables new connection established.
    try:
        async for message in websocket:
            data = json.loads(message)
            is_valid_user = check_valid_sid(data['uid'], data['sid'])
            if not is_valid_user:
                status = 0
                info = {}
            else:
                status = 1
                info = get_person_info(data['query_uid'])
            tosend = {'status': status, "info": info}
            tosend = json.dumps(tosend)
            await websocket.send(tosend)
    finally:
        pass
        # await unregister(websocket).
        # update local variables, connection broken.


def main():
    start_server = websockets.serve(communicate, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
