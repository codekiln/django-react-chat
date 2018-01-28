import graphene

from graphene_django.types import DjangoObjectType
from graphql.error import GraphQLLocatedError

from .models import ChatGroup, ChatMessage
from django_react_chat_example_project.users.models import User


class IntPkMixin(object):
    """
    convert all django pks to ints; by default they are serialized as string
    https://github.com/graphql-python/graphene-django/issues/383#issue-292197293
    """
    id = graphene.Int(source='pk')


class ChatGroupType(IntPkMixin, DjangoObjectType):
    class Meta:
        model = ChatGroup


class ChatMessageType(IntPkMixin, DjangoObjectType):
    author = graphene.Int()

    class Meta:
        model = ChatMessage

    def resolve_author(self, info):
        return self.author_id


class UserType(IntPkMixin, DjangoObjectType):
    is_current_user = graphene.Boolean()
    photo_url = graphene.String()
    name = graphene.String()

    class Meta:
        model = User

    def resolve_is_current_user(self, info):
        current_user = info.context.user
        if current_user:
            return self.id is current_user.id
        return False

    def resolve_photo_url(self, info):
        """
        Photo urls are currently not supported in back end.
        They are supported in the front end interface, though.
        Until they are supported, return the field if requested.
        """
        return ""

    def resolve_name(self, info):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        if self.first_name:
            return self.first_name
        name = getattr(self, 'name', None)
        if name:
            return name
        if self.username:
            return self.username
        return "User %s" % self.id


class ChatQuery(graphene.ObjectType):
    chat_group = graphene.Field(ChatGroupType, id=graphene.Int())
    chat_groups = graphene.List(ChatGroupType)

    chat_users = graphene.List(UserType)

    def resolve_chat_group(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return ChatGroup.objects.get(id=id)

        return None

    def resolve_chat_groups(self, info, **kwargs):
        return ChatGroup.objects.all()

    def resolve_chat_users(self, info, **kwargs):
        return User.objects.all()


schema = graphene.Schema(query=ChatQuery)
