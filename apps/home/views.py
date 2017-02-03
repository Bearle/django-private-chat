from django.views import generic
from braces.views import LoginRequiredMixin
from django.urls import reverse
from apps.chat import models
from apps.home.utils import get_silly_name
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings


class DialogListView(LoginRequiredMixin, generic.ListView):
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


class UserListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'landing/users.html'


class DialogRedirectView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        username = kwargs.pop('username')
        user = get_object_or_404(get_user_model(), username=username)
        new_dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
        url = reverse('dialog_list', kwargs={'pk': new_dialog.pk})
        return url
