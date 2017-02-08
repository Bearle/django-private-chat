from test_plus.test import TestCase
from apps.chat.models import *
from apps.chat.utils import *


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


class TestUtilsFunctions(TestCase):
    def setUp(self):
        self.user1 = self.make_user(username="user1")
        self.user2 = self.make_user(username="user2")

    def test_get_dialogs_with_user(self):
        self.dialog = Dialog()
        self.dialog.owner = self.user2
        self.dialog.opponent = self.user1
        self.dialog.save()
        dialog = get_dialogs_with_user(self.user1, self.user2)[0]
        self.assertEqual(dialog, self.dialog)

    # def test_get_user_from_session(self):
    #     sessions = Session.objects.all()
    #     required_session = None
    #     for session in sessions:
    #         session_data = session.get_decoded()
    #         uid = session_data.get('_auth_user_id')
    #         if uid == self.user1.id:
    #             required_session = session
    #             break
    #
    #     user = get_user_from_session(required_session.session_key)
    #     self.assertEqual(user, self.user1)