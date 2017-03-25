from django.db import models
from twilio import twiml
from rbot import stages
from rbot.stages import RBOT_STAGES, RBOT_STARTING_STAGE
from ridings.models import Riding

import importlib

STATUS = (('a', 'Active'), ('c', 'Completed'), ('f', 'Abandoned'))
REP_TYPES = (('mp', 'Federal'), ('mpp', 'Provincial'))
CONTACT_METHODS = (('email', 'Email'), ('phone', 'Phone'), ('fax', 'Fax'))


class Conversation(models.Model):
  phone_number = models.CharField(max_length=25)
  receiving_number = models.CharField(max_length=25)
  started = models.DateTimeField(auto_now_add=True)
  
  status = models.CharField(max_length=1, choices=STATUS, default='a', db_index=True)
  stage = models.CharField(max_length=25, choices=RBOT_STAGES.items(), blank=True, null=True, db_index=True)
  
  raw_name = models.CharField(max_length=255, blank=True, null=True)
  first_name = models.CharField(max_length=255, blank=True, null=True)
  last_name = models.CharField(max_length=255, blank=True, null=True)
  email = models.CharField(max_length=255, blank=True, null=True)
  postal_code = models.CharField(max_length=15, blank=True, null=True)
  
  representative = models.CharField(max_length=3, choices=REP_TYPES, blank=True, null=True)
  contact_method = models.CharField(max_length=15, choices=CONTACT_METHODS, blank=True, null=True)
  
  riding = models.ForeignKey(Riding, blank=True, null=True)
  topic = models.CharField(max_length=255, blank=True, null=True)
  message = models.TextField(blank=True, null=True)
  
  mailing_list_subscribed = models.BooleanField(default=False)
  
  
  def respond(self, incoming_message):
    # if no current stage, it means we have a new conversation...
    if not self.stage:
      next_stage = RBOT_STARTING_STAGE()
      preamble = None

    # otherwise, pass the incoming message to the current stage, and let it decide what to do      
    else:
      module = getattr(stages, self.stage)
      current_stage = getattr(module, RBOT_STAGES[self.stage])()
      next_stage, preamble = current_stage.respond(self, incoming_message.message)
    
    # set up sms response
    r = twiml.Response()
    
    # if the last step had a message, send it first
    if preamble:
      r.message(preamble)
      out_msg = SmsMessage(conversation=self,
                           outgoing=True,
                           message=preamble)
      out_msg.save()
      
    # then get (or re-send) any messages from the current step
    for m in next_stage.get_messages(self):
      r.message(m)
      out_msg = SmsMessage(conversation=self,
                           outgoing=True,
                           message=m)
      out_msg.save()

    # update the stage
    self.stage = next_stage.name
    self.save()
    
    # return the TwiML result
    return r

  
class SmsMessage(models.Model):
  conversation = models.ForeignKey(Conversation)
  timestamp = models.DateTimeField(auto_now_add=True)
  twilio_sid = models.CharField(max_length=255, blank=True, null=True, db_index=True)

  incoming = models.BooleanField(default=False, db_index=True)
  outgoing = models.BooleanField(default=False, db_index=True)

  message = models.TextField(blank=True, null=True)


