import graphene

from graphene_django.types import DjangoObjectType

from .models import ChatGroup, ChatMessage
from django_react_chat_example_project.users.models import User


class ChatGroupType(DjangoObjectType):
    class Meta:
        model = ChatGroup


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(object):
    chat_group = graphene.Field(ChatGroupType, id=graphene.Int())
    all_chat_groups = graphene.List(ChatGroupType)

    all_users = graphene.List(UserType)

    def resolve_chat_group(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return ChatGroup.objects.get(id=id)

        return None

    def resolve_all_chat_groups(self, info, **kwargs):
        return ChatGroup.objects.all()

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
