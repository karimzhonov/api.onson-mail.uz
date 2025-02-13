import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class QrCodeSessionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        await self.channel_layer.group_add(
            f'qrcode_session_{user.id}',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        await self.channel_layer.group_discard(
            f'qrcode_session_{user.id}',
            self.channel_name
        )

    async def send_message(self, event):
        message = event["message"]
        await self.send_json(message)


def send_data_to_session(user_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'qrcode_session_{user_id}', {
            'type': 'send.message',
            'message': data,
        }
    )