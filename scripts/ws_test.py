import json
import random
import socket
import time
from multiprocessing import Process

from websocket import create_connection


def f():
    for i in range(1000):
        ws = create_connection(
            'ws://localhost:8089/ws/users/',
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

def f2():
    ws = create_connection(
        'ws://localhost:8089/ws/users/',
        sockopt=(
            (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),
        )
    )
    for i in range(50):
        big_payload = "p"*999999
        ws.send(payload=json.dumps({"text": "hello_world", "big_payload": big_payload}))
        resp = ws.recv()
        print(i, len(resp))
        time.sleep(1)
    ws.close()


if __name__ == '__main__':
    for i in range(1):
        p = Process(target=f2)
        p.start()
