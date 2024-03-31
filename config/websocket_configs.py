import json
from uuid import UUID
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class CustomAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    # override encode_json to use UUIDEncoder
    async def encode_json(self, content):
        return json.dumps(content, cls=UUIDEncoder)

    async def send_message(self, data=None):
        # Send message to room group
        await self.send_json({"data": data})

    async def disconnect(self, close_code):
        # Leave room group & close connections
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )
