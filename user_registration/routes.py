from django.urls import re_path
from .consumer import *

websocket_urlpatterns = [
    re_path(r'^ws/transaction/(?P<user_id>\w+)/$', GameClockConsumer.as_asgi()),
    re_path(r'^ws/transaction/', GameClockConsumer.as_asgi()),
]