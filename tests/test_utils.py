from test_plus.test import TestCase
from django_private_chat.utils import *


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
