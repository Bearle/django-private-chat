# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_private_chat.urls import urlpatterns as django_private_chat_urls

urlpatterns = [
    url(r'^', include(django_private_chat_urls, namespace='django_private_chat')),
]
