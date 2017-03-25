from django.db import models

from rbot.models import Conversation

class PhoneCall(models.Model):
  conversation = models.ForeignKey(Conversation)

  call_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
  call2_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)

  from_number = models.CharField(max_length=255, blank=True, null=True)
  to_number = models.CharField(max_length=255, blank=True, null=True)

  requested = models.DateTimeField(blank=True, null=True)
  connected = models.DateTimeField(blank=True, null=True)
  completed = models.DateTimeField(blank=True, null=True)
  completed2 = models.DateTimeField(blank=True, null=True)

  duration = models.IntegerField(blank=True, null=True)
  duration2 = models.IntegerField(blank=True, null=True)

  call_status = models.CharField(max_length=255, blank=True, null=True)
  call_status2 = models.CharField(max_length=255, blank=True, null=True)

