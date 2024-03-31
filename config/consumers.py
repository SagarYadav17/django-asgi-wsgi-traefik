from config.websocket_configs import CustomAsyncJsonWebsocketConsumer


class ChatConsumer(CustomAsyncJsonWebsocketConsumer):
    # create universal group for all users
    group_name = "chat"

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send_json({"status": "connected"})

    async def receive_json(self, content, **kwargs):
        # receive message from user
        message = content.get("message")
        # send message to all users
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": message,
            },
        )

    async def chat_message(self, event):
        # receive message from group
        message = event.get("message")
        # send message to user
        await self.send_json({"message": message})
