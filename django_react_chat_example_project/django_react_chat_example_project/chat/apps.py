from __future__ import unicode_literals

from django.apps import AppConfig


class AdminChatConfig(AppConfig):
    name = 'django_react_chat_example_project.chat'
    verbose_name = "Chat"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
