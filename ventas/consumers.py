import json
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer


class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'GeeksforGeeks'
        }))
        # return super().connect()
    

    def disconnect(self, close_code):
        print("Desconectado")
        # return super().disconnect(close_code)
    

    def receive(self, text_data):
        print("Recibido " + text_data)

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(message)

        self.send(text_data=json.dump({ 'message':message}))

        return super().receive(text_data, bytes_data)



class DatosConsumer(AsyncConsumer):
    async def connect(self):
        await self.channel_layer.group_add("datos_actualizados", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("datos_actualizados", self.channel_name)

    async def datos_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))