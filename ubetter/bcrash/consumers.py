# # yourapp/consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ScrapingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def update_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({'message': message}))

# consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ScrapingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Handle the received message as needed
#         print(f"Received message: {message}")

#         # You can also send a response back if needed
#         await self.send(text_data=json.dumps({'message': 'Message received successfully'}))

#     async def update_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({'message': message}))


# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ScrapingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('result', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # pass
        await self.channel_layer.group_discard('result', self.channel_name)

    async def send_info(self, event):
        msg = event['message']
        await self.send(msg)
    async def receive(self, text_data):
        try:
            print(text_data)
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')

            # Handle the received message as needed
            print(f"Received message: {message}")

            # You can also send a response back if needed
            await self.send(text_data=json.dumps({'message': 'Message received successfully'}))
        except json.JSONDecodeError:
            print("Invalid asdfasdf JSON received:", text_data)
