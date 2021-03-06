from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/pages/(?P<room_id>\w+)/$", consumers.WebsiteConsumer),
    re_path(r"ws/chat/$", consumers.ChatConsumer),
]
