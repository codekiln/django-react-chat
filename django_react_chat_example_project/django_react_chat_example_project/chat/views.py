import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class JsContextMixin(object):

    @classmethod
    def add_js_context_to_context(cls, context, js_context_dict, key='js_context'):
        """
        Call this to serialize js_context into the context
        in the key 'js_context'. Merges js_context into
        the existing key 'js_context' in context.

        :param context: var to add js_context to
        :param js_context_dict: dict to serialize
        :param key: the key to store in the context dictionary
        :return: dictionary to be serialized to JSON
        """
        existing_js_context_json = context.get('js_context', {})
        try:
            existing_js_context_dict = json.loads(existing_js_context_json)
        except TypeError:
            # there was not any JSON in existing_js_context_json
            existing_js_context_dict = existing_js_context_json
        existing_js_context_dict.update(js_context_dict)
        new_js_context_json = json.dumps(existing_js_context_dict,
                                         sort_keys=True, indent=4)
        context.update({key: new_js_context_json})
        return context


class OldChatView(LoginRequiredMixin, TemplateView, JsContextMixin):
    template_name = "chat/old_chat_page.html"

    def get_context_data(self, **kwargs):
        context = super(OldChatView, self).get_context_data(**kwargs)
        js_context = {
            # named after the webpack bundle
            'chat.old_chat': {
                'chatWebsocketEndpoint': 'ws://localhost:8000/chat/',
            }
        }
        self.add_js_context_to_context(context, js_context)

        return context


class ChatView(LoginRequiredMixin, TemplateView, JsContextMixin):
    template_name = "chat/chat_page.html"

    def get_context_data(self, **kwargs):
        context = super(ChatView, self).get_context_data(**kwargs)
        js_context = {
            # named after the webpack bundle
            'chat.admin_chat': {
                'chatWebsocketEndpoint': 'ws://localhost:8000/chat/',
            }
        }
        self.add_js_context_to_context(context, js_context)

        return context
