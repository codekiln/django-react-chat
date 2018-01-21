from django.db import models
from django.db.models import fields

from django_react_chat_example_project.users.models import User


def get_chat_users_queryset():
    return User.objects.all()


class ChatGroup(models.Model):
    users = models.ManyToManyField(User)


class ChatMessage(models.Model):
    text = fields.TextField()
    author = models.ForeignKey(User)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="messages")
