from channels.generic.websockets import JsonWebsocketConsumer

from .schema import schema


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
                notify_user_ids = set([])
                for notify_key in ['createMessage', 'createGroup']:
                    if notify_key in result.data:
                        notify_user_ids |= set(result.data[notify_key].get('notifyUserIds', []))
                if notify_user_ids:
                    reply_user_ids = list(notify_user_ids)

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
