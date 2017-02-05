from django.views import generic
from braces.views import LoginRequiredMixin
from django.urls import reverse
from apps.chat import models
from apps.home.utils import get_silly_name
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q


class MessageListView(LoginRequiredMixin, generic.ListView):
    template_name = 'landing/home.html'
    model = models.Message
    ordering = 'created'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['silly_name'] = self.request.user.get_full_name()
        context['ws_server_path'] = 'ws://{}:{}/'.format(
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context


def get_dialogs_with_user(user_1, user_2):
    return models.Dialog.objects.filter(
        Q(owner=user_1, opponent=user_2) | Q(opponent=user_1, owner=user_2))


class DialogListView(LoginRequiredMixin, generic.ListView):
    template_name = 'landing/dialogs.html'
    model = models.Dialog
    ordering = 'modified'

    def get_queryset(self):
        dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
        return dialogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get('username'):
            # TODO: show alert that user is not found instead of 404
            user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
            dialog = get_dialogs_with_user(self.request.user, user)
            if len(dialog) == 0:
                dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
            else:
                dialog = dialog[0]
            context['active_dialog'] = dialog
        else:
            context['active_dialog'] = self.queryset[0]
        context['ws_server_path'] = 'ws://{}:{}/'.format(
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context


class UserListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'landing/users.html'
