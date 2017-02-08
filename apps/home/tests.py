from test_plus.test import TestCase
from apps.home.views import *
from django.test import RequestFactory
from django.urls import reverse
from apps.chat.models import *
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
        user = self.dialog.owner
        request = self.factory.get(reverse('dialogs_detail', kwargs={'username': 'opuser'}))
        request.user = user
        request.user.first_name = "Hey"
        request.user.last_name = "Dey"
        view.request = request
        view.object_list = Message.objects.all()
        view.kwargs = {}
        context = view.get_context_data()
        self.assertEqual(context['silly_name'],request.user.get_full_name())
        self.assertEqual(context['ws_server_path'],f"ws://{settings.CHAT_WS_SERVER_HOST}:{settings.CHAT_WS_SERVER_PORT}/")


class TestDialogListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner_user = self.make_user(username="owuser")
        self.oponet_user = self.make_user(username="opuser")
        self.dialog = Dialog()
        self.dialog.owner = self.owner_user
        self.dialog.opponent = self.oponet_user
        self.dialog.save()
        self.right_dialog = self.dialog
        self.dialog = Dialog()
        self.dialog.owner = self.make_user(username="user1")
        self.dialog.opponent = self.make_user(username="user2")
        self.dialog.save()

    def test_get_queryset(self):
        request = self.factory.get(reverse('dialogs_detail', kwargs={'username':'opuser'}))
        request.user = self.owner_user
        test_view = DialogListView()
        test_view.request = request
        queryset = list(test_view.get_queryset())
        required_queryset = [self.right_dialog]
        self.assertEqual(queryset, required_queryset)
