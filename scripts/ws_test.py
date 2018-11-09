import json
import random
import socket
import time
from multiprocessing import Process

from websocket import create_connection


def rand_sleep():
    time.sleep(random.randint(1, 20) * 0.1)


def f():
    for i in range(500):
        ws = create_connection(
            'ws://localhost:8087/ws/users/',
            sockopt=(
                (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),
            )
        )
        # rand_sleep()
        ws.send(payload=json.dumps({"text": "hello_world"}))
        # rand_sleep()
        resp = ws.recv()
        # rand_sleep()
        ws.close()
        print(i, resp)


if __name__ == '__main__':
    for i in range(25):
        p = Process(target=f)
        p.start()
