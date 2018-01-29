from channels.generic.websockets import JsonWebsocketConsumer

from .api_views import ChatUsersViewSet, ChatGroupsViewSet, ChatMessagesViewSet
from .schema import schema

class ChatActions(object):
    GET_CHAT_GROUPS = 'chatGroups'
    GET_USERS = 'chatUsers'
    CREATE_GROUP = 'createGroup'
    CREATE_MESSAGE = 'createMessage'


class ArtificialRequestContext(object):

    def __init__(self, user):
        self.user = user

    def get_context(self):
        return {
            'request': self
        }


def get_channel_group_name_for_user(user_id):
    return 'admin_chat_app_user_%s' % user_id


class ChatConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        user = self.message.user
        return [get_channel_group_name_for_user(user.id)]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        print("ws chat connect")
        self.message.reply_channel.send({"accept": True})

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        http_user = True
        reply = {}
        reply_user_ids = {self.message.user.id}
        print("ws chat receive %s" % self.message.user.id)

        request_context = ArtificialRequestContext(self.message.user)
        serializer_context = request_context.get_context()

        if 'gql' in content:
            graphql_query = content['gql']
            result = schema.execute(
                graphql_query, context_value=request_context)
            reply['gql'] = {
                "data": result.data,
                "errors": result.errors,
                "invalid": result.invalid
            }
            if result.data:
                # TODO: use graphql subscriptions instead of manual channels notifications
                if 'createMessage' in result.data:
                    notify_user_ids = result.data['createMessage'].get('notifyUserIds', None)
                    if notify_user_ids:
                        reply_user_ids = notify_user_ids

        if ChatActions.GET_USERS in content:
            users_serializer = ChatUsersViewSet.serializer_class(
                ChatUsersViewSet.queryset, many=True, context=serializer_context)
            reply[ChatActions.GET_USERS] = users_serializer.data

        if ChatActions.GET_CHAT_GROUPS in content:
            qs = ChatGroupsViewSet.queryset
            chat_groups_serializer = ChatGroupsViewSet.serializer_class(
                qs.filter(users=self.message.user), many=True, context=serializer_context)
            reply[ChatActions.GET_CHAT_GROUPS] = chat_groups_serializer.data

        if ChatActions.CREATE_GROUP in content:
            serializer_args = content[ChatActions.CREATE_GROUP]
            chat_groups_serializer = ChatGroupsViewSet.serializer_create_class(
                data=serializer_args, context=serializer_context)
            if chat_groups_serializer.is_valid():
                chat_groups_serializer.save()
                reply[ChatActions.CREATE_GROUP] = chat_groups_serializer.data

        if ChatActions.CREATE_MESSAGE in content:
            serializer_args = content[ChatActions.CREATE_MESSAGE]
            message_uuid = serializer_args.pop('uuid', '')
            chat_create_message_serializer = ChatMessagesViewSet.serializer_create_class(
                data=serializer_args, context=serializer_context)
            if chat_create_message_serializer.is_valid():
                chat_create_message_serializer.save()
                chat_group = chat_create_message_serializer.instance.chat_group
                reply_user_ids |= {u.id for u in chat_group.users.all()}
                reply[ChatActions.CREATE_MESSAGE] = chat_create_message_serializer.data
                reply[ChatActions.CREATE_MESSAGE]['uuid'] = message_uuid

        if reply:
            user_ids = list(reply_user_ids)
            print("ws chat receive: send reply %s" % ", ".join([str(uid) for uid in user_ids]))
            self.users_broadcast(user_ids, reply)

    @classmethod
    def user_send(cls, user_id, content, close=False):
        """
        Each chat user gets their own websocket Group.
        To message a user, you message that user's "group".
        """
        channel_group_name = get_channel_group_name_for_user(user_id)
        cls.group_send(channel_group_name, content, close=close)

    @classmethod
    def users_broadcast(cls, user_ids, content):
        for user_id in user_ids:
            cls.user_send(user_id, content)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        print("ws chat disconnect")
