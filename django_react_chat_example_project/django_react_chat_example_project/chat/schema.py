import json

import graphene
from graphene_django.types import DjangoObjectType

from django_react_chat_example_project.users.models import User
from .models import ChatGroup, ChatMessage


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
    chat_group = graphene.Int()

    class Meta:
        model = ChatMessage

    def resolve_author(self, info):
        return self.author_id

    def resolve_chat_group(self, info):
        return self.chat_group_id


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


class CreateMessage(graphene.Mutation):
    # return types
    status = graphene.Int()
    formErrors = graphene.String()
    chat_message = graphene.Field(ChatMessageType)
    uuid = graphene.String()

    # input types
    class Arguments:
        text = graphene.String()
        chat_group_id = graphene.Int()
        uuid = graphene.String()

    # the mutating function, with Arguments' input types coming after info
    def mutate(root, info, text, chat_group_id, uuid):
        if not info.context.user.is_authenticated():
            return CreateMessage(status=403)
        if not text:
            return CreateMessage(
                status=400,
                formErrors=json.dumps(
                    {'text': ['Please enter a message.']}))
        obj = ChatMessage.objects.create(
            author=info.context.user, text=text, chat_group=ChatGroup.objects.get(id=chat_group_id)
        )
        return CreateMessage(status=200, chat_message=obj, uuid=uuid)


class CreateGroup(graphene.Mutation):
    # return types
    status = graphene.Int()
    formErrors = graphene.String()
    chat_group = graphene.Field(ChatGroupType)

    # input types
    class Arguments:
        user_id = graphene.Int()

    # the mutating function, with Arguments' input types coming after info
    def mutate(root, info, user_id):
        if not info.context.user.is_authenticated():
            return CreateGroup(status=403)
        if not user_id:
            return CreateGroup(
                status=400,
                formErrors=json.dumps(
                    {'user_id': ['Please enter a user id.']}))
        user = User.objects.filter(id__in=[user_id]).first()
        if not user:
            return CreateGroup(status=400, formErrors=json.dumps(
                {'user_id': ['User id %s not found.' % user.id]}))
        group = ChatGroup.objects.filter(users=user).filter(users=info.context.user).first()
        if not group:
            group = ChatGroup.objects.create()
            group.save()
            group.users = [user, info.context.user]
            group.save()
        return CreateGroup(status=200, chat_group=group)


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


class ChatMutation(graphene.ObjectType):
    create_message = CreateMessage.Field()
    create_group = CreateGroup.Field()


schema = graphene.Schema(query=ChatQuery, mutation=ChatMutation)
