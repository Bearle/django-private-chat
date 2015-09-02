from django.conf import settings
from django.views import generic

from chat import models
from home.utils import get_silly_name


class HomePageView(generic.ListView):
    template_name = 'landing/home.html'
    model = models.ChatMessage
    ordering = 'created'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        silly_name = self.request.session.setdefault(
            'silly_name', get_silly_name()
        )
        context['silly_name'] = silly_name
        context['ws_server_path'] = 'ws://{}:{}/'.format(
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context





