import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .views import page_talks, page_about

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
                "type": "send_page_talks"
            }
        )

    async def disconnect(self, close_code):
        ''' Cliente se desconecta '''
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Load data
        data = json.loads(text_data)
        # Change page
        if data["action"] == "page":
            # Talks
            if data["value"] == "talks":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_page_talks"
                    }
                )
            # About
            if data["value"] == "about":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_page_about"
                    }
                )

    # Pages

    def _get_talks(self):
        return page_talks()

    async def send_page_talks(self, event):
        ''' Send Home page '''
        html = await sync_to_async(self._get_talks)()
        await self.send(text_data=html)

    def _get_about(self):
        return page_about()

    async def send_page_about(self, event):
        ''' Send About page '''
        html = await sync_to_async(self._get_about)()
        await self.send(text_data=html)