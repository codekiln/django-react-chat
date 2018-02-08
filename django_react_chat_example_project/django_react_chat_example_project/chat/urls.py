from django.conf.urls import url

from .views import RegularJsApolloChatView, ChatView

urlpatterns = [
    url(r'^$', ChatView.as_view(), name="chat_settings"),
    url(r'^regularJs$', RegularJsApolloChatView.as_view(), name="regular_js_chat"),
]
