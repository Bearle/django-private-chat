from test_plus.test import TestCase
from django_private_chat.views import *
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from django_private_chat.models import *


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
