import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .views import page_talks

class WebsiteConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        '''Connect user'''
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "root_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Send success connection
        await self.accept()

        # Send Home page
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "page_talks"
            }
        )

    async def disconnect(self, close_code):
        ''' Cliente se desconecta '''
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    def _get_talks(self):
        return page_talks()

    async def page_talks(self, event):
        ''' Send Home page '''
        html = await sync_to_async(self._get_talks)()
        await self.send(text_data=html)