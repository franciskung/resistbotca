from django.conf import settings
from django.db import models
from twilio import twiml
from twilio.rest import TwilioRestClient

from rbot import stages
from rbot.stages import RBOT_STARTING_STAGE
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
  stage = models.CharField(max_length=25, blank=True, null=True, db_index=True)
  
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
  
  def send_sms(self, msg, response=None):
    if response:
      response.message(msg)
      sms_id = None
    else:
      client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_AUTH)
      sms = client.messages.create(to=self.phone_number,
                                   from_=settings.TWILIO_NUMBER,
                                   body=msg)
      sms_id = sms.sid
      
    out_msg = SmsMessage(conversation=self,
                         outgoing=True,
                         message=msg,
                         twilio_sid=sms_id)
    out_msg.save()
  
  
  def respond(self, incoming_message):
    # if no current stage, it means we have a new conversation...
    if not self.stage:
      next_stage = RBOT_STARTING_STAGE()
      preamble = None

    # otherwise, pass the incoming message to the current stage, and let it decide what to do      
    else:
      module = importlib.import_module("rbot.stages.{0}".format(self.stage))
      current_stage = module.Stage()
      next_stage, preamble = current_stage.respond(self, incoming_message.message)
    
    # set up sms response
    r = twiml.Response()
    
    # if the last step had a message, send it first
    if preamble:
      self.send_sms(preamble, r)
      
    # then get (or re-send) any messages from the current step
    if next_stage:
      for m in next_stage.get_messages(self):
        self.send_sms(m, r)

      # if the current step has any other actions, perform them as well
      if hasattr(next_stage, "do_action"):
        next_stage.do_action(self, r)

      # update the stage
      self.stage = next_stage.name
      self.save()
    
    # if next step is null, it means we've reached the end of our journey.
    # but this shouldn't really happen...?
    else:
      # say goodbye, like a polite Canadian
      self.send_sms("Thanks, it's been a pleasure helping you. I hope we meet again soon!", r)
        
      # and do some internal clean-up
      self.status = 'c'
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


