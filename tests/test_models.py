#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-private-chat
------------

Tests for `django-private-chat` models module.
"""

from test_plus.test import TestCase
from django_private_chat.models import *


class DialogMethodTest(TestCase):

    def setUp(self):
        self.dialog = Dialog()
        self.dialog.owner = self.make_user(username="owuser")
        self.dialog.opponent = self.make_user(username="opuser")

    def test_str_method(self):
        self.assertEqual(str(self.dialog), "Chat with opuser")


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
        """
        Makes sure message text and something relating to the date
        is in the string function output
        """
        mes = str(self.message)
        text = self.message.text
        hour = self.message.modified.strftime('%H')
        tfhour = self.message.modified.strftime('%I')  # 24-hour clock
        min = self.message.modified.strftime('%M')
        day = self.message.modified.strftime('%d')
        month = self.message.modified.strftime('%m')
        lmon = self.message.modified.strftime('%b')  # month abbreviation
        self.assertTrue((text in mes) and
                        (hour in mes or tfhour in mes) and
                        (min in mes) and
                        (day in mes) and
                        (month in mes or lmon in mes))

    def test_soft_delete(self):
        msg = self.message
        self.message.delete()
        self.assertNotIn(msg, Message.objects.all())
        self.assertIn(msg, Message.all_objects.filter(is_removed=True))
