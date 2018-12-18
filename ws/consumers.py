import os
from datetime import datetime

import objgraph
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

ospid = os.getpid()


def save_objgraph_info():
    dt_iso = datetime.now().isoformat()
    with open('./logs/growth_{}.log'.format(ospid), 'a') as f:
        f.write("{}\n".format(dt_iso))
        objgraph.show_growth(limit=20, shortnames=False, file=f)

    with open('./logs/most_common_types_{}.log'.format(ospid), 'a') as f:
        f.write("{}\n".format(dt_iso))
        objgraph.show_most_common_types(limit=20, file=f)


class WsUsersConsumer(JsonWebsocketConsumer):
    def connect(self):
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
