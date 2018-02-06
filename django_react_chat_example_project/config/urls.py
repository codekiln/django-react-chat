import channels
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from django_react_chat_example_project.chat.schema import schema
from django_react_chat_example_project.chat.views import ChatView

urlpatterns = [
                  url(r'^$', ChatView.as_view(), name='home'),

                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL, admin.site.urls),

                  url(r'^gql_batched', csrf_exempt(GraphQLView.as_view(schema=schema, batch=True)), name="gql_batched"),
                  url(r'^graphql', GraphQLView.as_view(schema=schema, graphiql=True), name="graphiql"),
                  url(r'^gql', csrf_exempt(GraphQLView.as_view(schema=schema, batch=False)), name="gql"),

                  # Chat
                  url(r'^chat/', include('django_react_chat_example_project.chat.urls', namespace='chat')),

                  # User management
                  url(r'^users/', include('django_react_chat_example_project.users.urls', namespace='users')),
                  url(r'^accounts/', include('allauth.urls')),

                  # Your stuff: custom urls includes go here

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

channel_routing = [
    # Include sub-routing from apps
    channels.include("django_react_chat_example_project.chat.routing.chat_routing", path=r"^/chat"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
                          url(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
