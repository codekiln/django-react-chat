from django.utils.functional import SimpleLazyObject
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_react_chat_example_project.users.models import User
from .models import ChatGroup, ChatMessage, get_chat_users_queryset


class IsCurrentUserMixin(serializers.Serializer):
    # include in serializer to use
    # isCurrentUser = serializers.SerializerMethodField()

    def get_isCurrentUser(self, user):
        return self.is_current_user(user)

    def get_current_user(self):
        request = self.context.get("request")
        if request:
            if hasattr(request, "user"):
                return request.user
            try:
                return request['user']
            except IndexError:
                pass
        return None

    def get_current_user_instance(self):
        current_user = self.get_current_user()
        if current_user:
            if isinstance(current_user, SimpleLazyObject):
                return User.objects.get(id=current_user.id)
            return current_user
        return None

    def get_current_user_id(self):
        # if we pass the user directly to the context of the serializer,
        # then use that
        user = self.get_current_user()
        if user:
            return user.id
        return None

    def is_current_user(self, user):
        current_user_id = self.get_current_user_id()
        if current_user_id == user.id:
            return True
        return False


class UserNameMixin(object):
    def get_name(self, user):
        if user.first_name and user.last_name:
            return "%s %s" % (user.first_name, user.last_name)
        if user.first_name:
            return user.first_name
        name = getattr(user, 'name', None)
        if name:
            return name
        if user.username:
            return user.username
        return "User %s" % user.id


class ChatUserSerializer(IsCurrentUserMixin, UserNameMixin, serializers.ModelSerializer):
    isCurrentUser = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    photoUrl = serializers.SerializerMethodField()

    class Meta:
        model = User
        serializer_related_field = serializers.PrimaryKeyRelatedField(read_only=True)
        fields = (
            'id',
            'username',
            'name',
            'photoUrl',
            'isCurrentUser',
        )

    def get_photoUrl(self, user):
        return ""


class ChatGroupCreateSerializer(IsCurrentUserMixin, serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=get_chat_users_queryset())

    class Meta:
        model = ChatGroup
        fields = (
            'id',
            'users',
        )

    def validate_users(self, users):
        current_user = self.get_current_user_instance()
        if current_user not in users:
            users.append(current_user)
        if len(users) < 2:
            raise ValidationError("Chat Groups must have at least two users in them")
        return users

    def save(self, **kwargs):
        super(ChatGroupCreateSerializer, self).save(**kwargs)


class ChatGroupMessageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = (
            'id',
            'text',
            'author',
        )


class ChatGroupUserSerializer(IsCurrentUserMixin, UserNameMixin, serializers.ModelSerializer):
    isCurrentUser = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'isCurrentUser'
        )


class ChatGroupReadSerializer(serializers.ModelSerializer):
    users = ChatGroupUserSerializer(many=True, read_only=True)
    messages = ChatGroupMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatGroup
        fields = (
            'id',
            'messages',
            'users',
        )


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    chat_group = serializers.PrimaryKeyRelatedField(queryset=ChatGroup.objects.all())
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ChatMessage
        fields = (
            'id',
            'text',
            'author',
            'chat_group'
        )


class ChatMessageReadSerializer(serializers.ModelSerializer):
    chat_group = ChatGroupReadSerializer(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ChatMessage
        fields = (
            'id',
            'text',
            'author',
            'chat_group'
        )
