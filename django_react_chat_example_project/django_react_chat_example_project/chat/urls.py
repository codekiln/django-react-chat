from django.conf.urls import url

from .views import ChatView

urlpatterns = [
    url(r'^$', ChatView.as_view(), name="chat_settings"),
]
