from channels.generic.websocket import AsyncWebsocketConsumer
import json


class PriceUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"price_updates_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_price_update(self, event):
        """
        Send a price update to the WebSocket.
        """
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                }
            )
        )
