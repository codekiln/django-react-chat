from .models import ChatGroup, get_chat_users_queryset, ChatMessage
from .serializers import ChatGroupCreateSerializer, ChatUserSerializer, ChatMessageReadSerializer, ChatGroupReadSerializer, \
    ChatMessageCreateSerializer
from rest_framework.viewsets import ModelViewSet


class FlexibleSerializerMixin(object):
    def get_serializer_class(self):
        """
        return a different serializer if creating
        """
        action = getattr(self, 'action', None)
        if action == 'create' and hasattr(self, 'serializer_create_class'):
            return self.serializer_create_class
        return self.serializer_class


class ChatGroupsViewSet(FlexibleSerializerMixin, ModelViewSet):
    serializer_class = ChatGroupReadSerializer
    serializer_create_class = ChatGroupCreateSerializer
    # filter_backends = (DjangoFilterBackend,)
    queryset = ChatGroup.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return super(ChatGroupsViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(ChatGroupsViewSet, self).create(request, *args, **kwargs)


class ChatUsersViewSet(ModelViewSet):
    serializer_class = ChatUserSerializer
    queryset = get_chat_users_queryset()
    lookup_field = 'id'


class ChatMessagesViewSet(FlexibleSerializerMixin, ModelViewSet):
    serializer_class = ChatMessageReadSerializer
    serializer_create_class = ChatMessageCreateSerializer
    queryset = ChatMessage.objects.all()

    def create(self, request, *args, **kwargs):
        """
        {
            author: "1x",
            text: "this is a test of chatting",
            chat_group: {
                users: ["1x", "3x"]
            }
        }
        """
        return super(ChatMessagesViewSet, self).create(request, *args, **kwargs)
