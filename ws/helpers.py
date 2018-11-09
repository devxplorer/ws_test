import channels.layers
from asgiref.sync import async_to_sync


def send_message(user_id, msg_type, msg='', **kwargs):
    if not user_id:
        return

    kwargs.update({
        'type': msg_type,
        'body': msg
    })

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('user_{}'.format(user_id), {
        'type': 'user_message',
        'payload': kwargs
    })
