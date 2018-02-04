from django.conf.urls import url

from .views import OldChatView

urlpatterns = [
    url(r'^$', OldChatView.as_view(), name="chat_settings"),
    url(r'^old$', OldChatView.as_view(), name="old_chat")
]
