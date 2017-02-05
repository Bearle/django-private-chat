# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^users/$',
        view=views.UserListView.as_view(),
        name='list'
    ),
# url(
#         regex=r'^(?P<username>[\w.@+-]+)/$',
#         view=views.UserDetailView.as_view(),
#         name='detail'
#     ),
    url(
        regex=r'^dialogs/(?P<pk>[0-9]+)$',
        view=views.MessageListView.as_view(),
        name='dialog_list'
    ),
    url(
        regex=r'^dialogs/(?P<username>[\w.@+-]+)$',
        view = views.DialogListView.as_view(),
        name='dialogs_detail'
    ),
    url(
        regex=r'^dialogs/$',
        view = views.DialogListView.as_view(),
        name='dialogs'
    ),
    # url(r'^$',
    #     views.HomePageView.as_view(),
    #     name='home'
    # ),
]
