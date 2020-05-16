import sqlite3
import time

conn = sqlite3.connect("/tmp/data.db")
c = conn.cursor()

c.execute("""SELECT * FROM users""")
print(c.fetchall())


def add_message_to_channel(uid, msg, channel):
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute(
                f"INSERT INTO {channel} VALUES (:username, :msg, :time)",
                {"username": uid, "msg": msg, "time": time.time()},
            )
    conn.commit()
    conn.close()


add_message_to_channel('dhananjay', 'hello everyone', 'channel1')

c.execute("""SELECT * FROM channel1""")
print(c.fetchall())

c.execute("""SELECT * FROM members""")
print(c.fetchall())


def register_sid(sid, username):
    # TODO store sid to db
    expiry = time.time() + (24 * 60 * 60)
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("""INSERT INTO active VALUES (:uid, :sid, :expiry)""",
              {'uid': username, 'sid': sid, 'expiry': expiry})
    conn.commit()
    conn.close()


register_sid('sadasdasdas', 'dhananjay')
c.execute("""SELECT * FROM active""")
print(c.fetchall())


def check_db(username, password):
    #  TODO
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE username=:name AND transformedpass=:pass""",
              {'name':username, 'pass': password})
    count = len(c.fetchall())
    conn.close()
    if count > 0:
        return True
    else:
        return False


print(check_db('dhananjay', 'passdhananjay'))


def get_list_of_channels(uid):
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("""SELECT channelname FROM members WHERE username=:name""",
              {'name': uid})
    channel_list = [i[0] for i in c.fetchall()]
    conn.commit()
    conn.close()
    return channel_list


print(get_list_of_channels('dhananjay'))


def get_person_info(uid):
    #  TODO get person info
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("""SELECT username, display FROM users WHERE username=:name""",
              {'name': uid})
    res = c.fetchone()
    if len(res) == 0:
        res = ['', '']
    info = {
        "username": res[0],
        "display-name": res[1],
        "icon_link": ""
    }
    conn.commit()
    conn.close()
    return info


print(get_person_info('sahil'))


def get_messages_from_channel(uid, sid, channel):
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM " + channel + " ORDER BY time DESC LIMIT 1;""",
              {'name': uid})
    ls = c.fetchall()
    conn.commit()
    conn.close()
    return ls


print(get_messages_from_channel('', '', 'channel1'))


def is_valid_send_request(uid, channel):
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute(""" SELECT * FROM members
    WHERE username=:name AND channelname=:ch""", {'name': uid, 'ch': channel})
    count = len(c.fetchall())
    conn.close()
    if count >= 0:
        return True
    else:
        return False


print(is_valid_send_request('dhananjay', 'channel1'))


def get_users_in_channel(channel):
    conn = sqlite3.connect('/tmp/data.db')
    c = conn.cursor()
    c.execute("SELECT username FROM members WHERE channelname=:ch""",
              {'ch': channel})
    ls = [i[0] for i in c.fetchall()]
    conn.commit()
    conn.close()
    return ls


print(get_users_in_channel('channel2'))

conn.commit()
conn.close()
