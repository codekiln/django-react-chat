from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import api_views
from .views import ChatView

urlpatterns = [
    url(r'^$', ChatView.as_view(), name="chat_settings"),
]

router = SimpleRouter()
router.register(
    prefix=r'groups',
    viewset=api_views.ChatGroupsViewSet,
    base_name='chat_groups')
router.register(
    prefix=r'users',
    viewset=api_views.ChatUsersViewSet,
    base_name='chat_users')
router.register(
    prefix=r'messages',
    viewset=api_views.ChatMessagesViewSet,
    base_name='chat_messages')


urlpatterns += router.urls
