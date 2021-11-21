import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .views import page_talks, page_about, page_single_talk, page_results, page_profiles


class WebsiteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect user"""
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
                "type": "send_page_talks",
                "page": 1,
            },
        )

    async def disconnect(self, close_code):
        """Cliente se desconecta"""
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Load data
        data = json.loads(text_data)
        # Change page
        if data["action"] == "page":
            # Talks
            if data["value"] == "talks":
                page = 1
                if "page" in data:
                    page = int(data["page"])
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_page_talks",
                        "page": page,
                    },
                )
            # Single talk
            if data["value"] == "single-talk":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_page_single_talk",
                        "id": data["id"],
                    },
                )
            # Profiles
            if data["value"] == "profiles":
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "send_page_profiles"}
                )

            # About
            if data["value"] == "about":
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "send_page_about"}
                )

            # Search
            if data["value"] == "search-talks":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_page_search",
                        "search": data["search"],
                    },
                )

    # Pages

    def _get_talks(self, page=1):
        return page_talks(page=page)

    async def send_page_talks(self, event):
        """Send Home page"""
        html = await sync_to_async(self._get_talks)(event["page"])
        await self.send(text_data=html)

    def _get_single_talk(self, id):
        return page_single_talk(id)

    async def send_page_single_talk(self, event):
        """Send Single talk page"""
        html = await sync_to_async(self._get_single_talk)(event["id"])
        await self.send(text_data=html)

    def _get_profiles(self):
        return page_profiles()

    async def send_page_profiles(self, event):
        """Send Profiles page"""
        html = await sync_to_async(self._get_profiles)()
        await self.send(text_data=html)

    def _get_about(self):
        return page_about()

    async def send_page_about(self, event):
        """Send About page"""
        html = await sync_to_async(self._get_about)()
        await self.send(text_data=html)

    def _get_results(self, search):
        return page_results(search)

    async def send_page_search(self, event):
        """Send results talks"""
        if event["search"] != "":
            html = await sync_to_async(self._get_results)(event["search"])
        else:
            html = await sync_to_async(self._get_talks)()
        await self.send(text_data=html)
