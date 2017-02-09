# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Message,
	Dialog,
)


class MessageCreateView(CreateView):

    model = Message


class MessageDeleteView(DeleteView):

    model = Message


class MessageDetailView(DetailView):

    model = Message


class MessageUpdateView(UpdateView):

    model = Message


class MessageListView(ListView):

    model = Message


class DialogCreateView(CreateView):

    model = Dialog


class DialogDeleteView(DeleteView):

    model = Dialog


class DialogDetailView(DetailView):

    model = Dialog


class DialogUpdateView(UpdateView):

    model = Dialog


class DialogListView(ListView):

    model = Dialog

