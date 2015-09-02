from django.db import models
from django_extensions.db import models as dj_extensions_models


class ChatMessage(dj_extensions_models.TimeStampedModel):
    username = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()


class UserEvent(dj_extensions_models.TimeStampedModel):
    user_name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
