import json

import django_filters
import graphene
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id

from django_react_chat_example_project.users.models import User
from .models import ChatGroup, ChatMessage


class ChatGroupType(DjangoObjectType):
    class Meta:
        model = ChatGroup
        interfaces = (graphene.Node,)


class UserType(DjangoObjectType):
    is_current_user = graphene.Boolean(required=True)
    photo_url = graphene.String(required=True)
    name = graphene.String(required=True)
    abbreviation = graphene.String(required=True)

    class Meta:
        model = User
        # filter_fields = ['is_current_user']
        # interfaces = (graphene.relay.Node,)
        interfaces = (graphene.Node,)

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

    def resolve_abbreviation(self, info):
        """
        The abbreviation to use in the avatar for this user
        """
        if self.first_name and self.last_name:
            return "%s%s" % (
                self.first_name[0].upper(),
                self.last_name[0].upper())
        if self.first_name:
            return self.first_name[:2].upper()
        name = getattr(self, 'name', None)
        if name:
            return name[:2].upper()
        if self.username:
            return self.username[:2].upper()
        # "No Username"
        return "NU"


# currently, the request object is not supplied to filtersets in
# django-graphene 2.0.0 - https://github.com/graphql-python/graphene-django/issues/399
# filtering by current user won't happen until the request is passed
# class UserFilter(django_filters.FilterSet):
#     only_other_users = django_filters.BooleanFilter(method='filter_only_other_users')
#
#     def __init__(self, *args, **kwargs):
#         super(UserFilter, self).__init__(args, kwargs)
#
#     class Meta:
#         model = User
#         fields = ['only_other_users']
#
#     def filter_only_other_users(self, queryset, name, value):
#         if name == 'only_other_users':
#             show_only_other_users = value
#             user = self.request.user
#             if user and show_only_other_users:
#                 return queryset.filter(~Q(id=user.id))
#         return queryset


class ChatMessageType(DjangoObjectType):
    author = graphene.Field(UserType, required=True)
    # chat_group = graphene.Field(ChatGroupType)

    class Meta:
        model = ChatMessage
        interfaces = (graphene.Node,)

    # def resolve_author(self, info):
    #     return self.author
    #
    # def resolve_chat_group(self, info):
    #     return self.chat_group_id


# class CreateMessage(graphene.Mutation):
#     # return types
#     status = graphene.Int()
#     formErrors = graphene.String()
#     chat_message = graphene.Field(ChatMessageType)
#     uuid = graphene.String()
#     notify_user_ids = graphene.List(graphene.Int)
#
#     # input types
#     class Arguments:
#         text = graphene.String()
#         chat_group_id = graphene.Int()
#         uuid = graphene.String()
#
#     # the mutating function, with Arguments' input types coming after info
#     def mutate(root, info, text, chat_group_id, uuid):
#         if not info.context.user.is_authenticated():
#             return CreateMessage(status=403)
#         if not text:
#             return CreateMessage(
#                 status=400,
#                 formErrors=json.dumps(
#                     {'text': ['Please enter a message.']}))
#         group = ChatGroup.objects.filter(id=chat_group_id).first()
#         if not group:
#             return CreateMessage(
#                 status=400,
#                 formErrors=json.dumps(
#                     {'chat_group_id': ['Chat Group Not Found: %s.' % chat_group_id]}))
#         obj = ChatMessage.objects.create(
#             author=info.context.user, text=text, chat_group=group
#         )
#         notify_user_ids = group.users.values_list('id', flat=True)
#         return CreateMessage(status=200, chat_message=obj, uuid=uuid,
#                              notify_user_ids=notify_user_ids)


# class CreateGroup(graphene.Mutation):
#     # return types
#     status = graphene.Int()
#     formErrors = graphene.String()
#     chat_group = graphene.Field(ChatGroupType)
#     notify_user_ids = graphene.List(graphene.Int)
#
#     # input types
#     class Arguments:
#         user_id = graphene.Int()
#
#     # the mutating function, with Arguments' input types coming after info
#     def mutate(root, info, user_id):
#         if not info.context.user.is_authenticated():
#             return CreateGroup(status=403)
#         if not user_id:
#             return CreateGroup(
#                 status=400,
#                 formErrors=json.dumps(
#                     {'user_id': ['Please enter a user id.']}))
#         user = User.objects.filter(id__in=[user_id]).first()
#         if not user:
#             return CreateGroup(status=400, formErrors=json.dumps(
#                 {'user_id': ['User id %s not found.' % user.id]}))
#         group = ChatGroup.objects.filter(users=user).filter(users=info.context.user).first()
#         group_users = [user, info.context.user]
#         if not group:
#             group = ChatGroup.objects.create()
#             group.save()
#             group.users = group_users
#             group.save()
#         return CreateGroup(
#             status=200, chat_group=group,
#             notify_user_ids=[u.id for u in group_users])


class ChatQuery(graphene.ObjectType):

    current_user = graphene.Field(UserType)

    def resolve_current_user(self, info, **kwargs):
        if not info.context.user.is_authenticated():
            return None
        return info.context.user

    chat_group = graphene.Field(ChatGroupType, id=graphene.ID())

    def resolve_chat_group(self, info, **kwargs):
        rid = from_global_id(kwargs.get('id'))
        return ChatGroup.objects.get(pk=rid[1])

    chat_groups = graphene.List(ChatGroupType)

    def resolve_chat_groups(self, info, **kwargs):
        return ChatGroup.objects.all()

    chat_users = graphene.List(UserType)

    def resolve_chat_users(self, info, **kwargs):
        return User.objects.all()


# class ChatMutation(graphene.ObjectType):
    # create_message = CreateMessage.Field()
    # create_group = CreateGroup.Field()


schema = graphene.Schema(
    query=ChatQuery
    # , mutation=ChatMutation
)
