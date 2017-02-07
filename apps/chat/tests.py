from test_plus.test import TestCase
from apps.chat.models import *


class DialogMethodTest(TestCase):
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.owner = self.make_user(username="owuser")
        self.dialog.opponent = self.make_user(username="opuser")

    def test_str_method(self):
        self.assertEqual(str(self.dialog), "Диалог с opuser")


class MessageMethodTest(TestCase):
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.owner = self.make_user(username="owuser")
        self.dialog.opponent = self.make_user(username="opuser")
        self.dialog.save()
        self.message = Message()
        self.message.dialog = self.dialog
        self.message.sender = self.dialog.owner
        self.message.text = "text about something interesting"
        self.message.save()

    def test_str_method(self):
        self.assertEqual(str(self.message), "owuser(" +
                         self.message.modified.strftime('%x %X') + ") - 'text about something interesting'")

    def test_soft_delete(self):
        msg = self.message
        self.message.delete()
        self.assertNotIn(msg, Message.objects.all())
        self.assertIn(msg, Message.all_objects.filter(is_removed=True))
