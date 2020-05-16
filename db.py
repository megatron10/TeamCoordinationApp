import sqlite3
import random
import time

conn = sqlite3.connect("/tmp/data.db")
c = conn.cursor()

c.execute(
    """ CREATE TABLE users (
        username text,
        display text,
        transformedpass text
        )
        """
)

c.execute(
    """ CREATE TABLE active(
        uid text,
        sid text,
        expiry integer
    )
    """
)

c.execute(
    """ CREATE TABLE online(
        uid text
    )
    """
)

c.execute(
    """ CREATE TABLE members (
        username text,
        channelname text
    )
    """
)

channels = [f"channel{i}" for i in range(9)]

for ch in channels:
    c.execute(f"CREATE TABLE {ch} (senderid text, message text, time integer)")

users = [
    ("dhananjay", "Dhananjay Raut"),
    ("sahil", "Sahil Shah"),
    ("vijay", "Vijay Tadikamalla"),
]

for i, j in users:
    c.execute(
        "INSERT INTO users VALUES (:username, :dpname, :pass)",
        {"username": i, "dpname": j, "pass": "pass" + i},
    )

for ch in channels:
    for i, _ in users:
        if random.random() < 0.7:
            c.execute(
                "INSERT INTO members VALUES (:username, :chname)",
                {"username": i, "chname": ch},
            )
            c.execute(
                f"INSERT INTO {ch} VALUES (:username, :msg, :time)",
                {"username": i, "msg": "hi", "time": time.time()},
            )
conn.commit()
conn.close()
