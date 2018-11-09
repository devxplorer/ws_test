import gc
import os
import random
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

GC_RUN_CHANCE_PERCENTAGES = 10


def gc_collect_with_chance(percentages_chance):
    ospid = os.getpid()
    if random.randint(1, 100) <= percentages_chance:
        with open('./logs/gc_collect_run.log'.format(ospid), 'a') as f:
            f.write("{} ({})\n".format(datetime.now().isoformat(), ospid))
        gc.collect()


def save_objgraph_info():
    with open('./logs/growth_{}.log'.format(ospid), 'a') as f:
        # with open('./logs/most_common_types.log', 'wa') as f:
        f.write("{}\n".format(datetime.now().isoformat()))
        objgraph.show_growth(limit=20, shortnames=False, file=f)
        # objgraph.show_most_common_types(limit=20, file=f)


class WsUsersConsumer(JsonWebsocketConsumer):
    def connect(self):
        # gc_collect_with_chance(GC_RUN_CHANCE_PERCENTAGES)
        # save_objgraph_info()

        self.user = self.scope['user']
        self.session = self.scope['session']
        if self.user.is_authenticated:
            self.user_group = 'user_{}'.format(self.user.id)

            async_to_sync(self.channel_layer.group_add)(
                self.user_group,
                self.channel_name
            )

        self.accept()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.user_group,
                self.channel_name
            )

    # Receive message from WebSocket
    def receive_json(self, content, **kwargs):
        self.send_json(content)

    # Receive message from channel layer
    def user_message(self, event_data):
        payload = event_data['payload']

        # Send message to WebSocket
        self.send_json(payload)
