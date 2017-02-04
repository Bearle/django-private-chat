from test_plus.test import TestCase
from .views import *
from django.test import RequestFactory
from django.urls import reverse
from ..chat.models import *
from django.conf import settings

class ViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.dialog = Dialog()
        self.dialog.owner = self.make_user(username="owuser")
        self.dialog.opponent = self.make_user(username="opuser")
        self.dialog.save()

    def test_message_list_context(self):
        view = MessageListView(template_name='landing/home.html', model=Message)
        request = self.factory.get(reverse('dialog_list', kwargs={'pk': self.dialog.pk}))
        request.user = self.make_user("someuser")
        request.user.first_name = "Hey"
        request.user.last_name = "Dey"
        view.request = request
        view.object_list = Message.objects.all()
        view.kwargs = {}
        context = view.get_context_data()
        self.assertEqual(context['silly_name'],request.user.get_full_name())
        self.assertEqual(context['ws_server_path'],f"ws://{settings.CHAT_WS_SERVER_HOST}:{settings.CHAT_WS_SERVER_PORT}/")

