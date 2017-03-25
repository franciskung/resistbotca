from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import re

from rbot.models import Conversation, SmsMessage
from rbot.easter_eggs import EGGS

START_KEYWORDS = ('resist','hello',)


@csrf_exempt
def handle_sms(request):

  # clean up phone numbers  
  from_number = re.sub('[^0-9]', '', request.POST.get('From', ""))
  to_number = re.sub('[^0-9]', '', request.POST.get('To', ""))
  
  # see if this message is part of an existing converation
  conversation = Conversation.objects.filter(phone_number=from_number, receiving_number=to_number, status='a').first()
  
  # create a conversation if none exists, or if a START_KEYWORD was used
  if request.POST.get('Body', '').lower() in START_KEYWORDS or not conversation:
  
    if conversation:
      conversation.status = 'f'
      conversation.save()
      
    conversation = Conversation(phone_number=from_number, receiving_number=to_number)
    conversation.save()

  # log the incoming message
  message = SmsMessage(conversation=conversation,
                       twilio_sid=request.POST.get('MessageSid'),
                       incoming=True,
                       message=request.POST.get('Body'))
  message.save()
    
    
  # let's have some fun and add some easter eggs ;)
  # (but only send one message max)
  egged = False
  answer = None
  for keyword, easteregg in EGGS.items():
    if keyword.lower() in message.message.lower() and not egged:
      conversation.send_sms(easteregg)
      egged = True
      # TODO: we'll probably want a way to disable some of these, ie for the open-text-entry of an email message
  
  # or, a more serious next step
  # (but only if an easter egg hasn't already been sent...)
  if not egged:
    answer = conversation.respond(message)
  
  if answer:
    return HttpResponse(str(answer))
  else:
    return HttpResponse("")

