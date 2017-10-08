"""
ResistbotCA

Copyright (c) 2017 franciskung.com consulting ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. 
"""


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

