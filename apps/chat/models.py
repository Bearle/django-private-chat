from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.defaultfilters import date as dj_date


class Dialog(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Владелец диалога", related_name="selfDialogs")
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Собеседник владельца")

    def __str__(self):
        return f"Диалог с {self.opponent.username}"


class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, verbose_name="Диалог", related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Автор", related_name="messages")
    text = models.TextField(verbose_name="Текст сообщения")
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.sender.username}({self.modified.strftime('%x %X')}) - '{self.text}'"

    def get_formatted_create_datetime(self):
        return dj_date(self.created, settings.DATETIME_FORMAT)
