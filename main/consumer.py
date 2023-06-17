from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ReserveConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connection")
        await self.channel_layer.group_add('my_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(f'Connection closed with code: {close_code} ')
        await self.channel_layer.group_discard('my_group', self.channel_name)


    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # sender = text_data_json["sender"]
        print("Main consumer recived")
        
        print(message)

        await self.send(text_data=json.dumps({
            'message': message,
            # 'sender': sender
        }))

        await self.channel_layer.group_send(
            'my_group',
            {'type': 'reserve_message',
            'message': message}
        )

    async def reserve_message(self, event):
        # Receive the message sent to the group
        print("ReserveConsumer got my_message --> PASSING")
        pass

class MyCafeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connection")
        await self.channel_layer.group_add('my_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(f'Connection closed with code: {close_code} ')
        await self.channel_layer.group_discard('my_group', self.channel_name)


    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # sender = text_data_json["sender"]
        print("My cafe update recieved consumer recived")        
        print(message)
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def reserve_message(self, event):
        # Receive the message sent to the group
        print("MyCafe got my_message --> UPDATING!")
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))
