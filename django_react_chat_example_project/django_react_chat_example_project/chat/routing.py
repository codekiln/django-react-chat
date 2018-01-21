from channels.routing import route_class

from .consumers import ChatConsumer

chat_routing = [
    route_class(ChatConsumer),
]
