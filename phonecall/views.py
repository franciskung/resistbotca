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


from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from twilio import twiml, TwilioRestException
from twilio.rest import TwilioRestClient

from rbot.models import SmsMessage

import time

from phonecall.models import PhoneCall

# starts a phone call (called in response to an SMS, not directly over the web)
def start_call(conversation):

  # pause, as requested
  time.sleep(6)
  
  # try making the outgoing call
  client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_AUTH)
  try:
    call = client.calls.create(to=conversation.phone_number,
                               from_=settings.TWILIO_NUMBER,
                               url="{0}{1}".format(settings.SITE_URL, reverse('phone_twilio')),
                               status_callback="{0}{1}".format(settings.SITE_URL, reverse('phone_twilio_completed2')))

    # log the call so we can be sane and track it
    phonecall = PhoneCall(conversation=conversation,
                          call_id=call.sid,
                          from_number=conversation.phone_number,
                          to_number=conversation.riding.representative_phone,
                          requested=timezone.now())
    phonecall.save()

    return True
    
  # didn't work. shucks.    
  except TwilioRestException as e:
    #print e

    converastion.send_sms("hmm, I wasn't able to call you. Bugs in the system? Sorry about that, please try again later.")
    
    return False


# twilio callback for when they successfully connect to the user
@csrf_exempt
def twilio(request):
  answer = twiml.Response()
  phonecall = PhoneCall.objects.filter(call_id=request.POST.get('CallSid')).first()

  if phonecall:

    conversation = phonecall.conversation
    phonecall.connected = timezone.now()
    phonecall.save()

    answer.pause(length=2)
    answer.say(u"Hello, {0}. I'm here to help you call your MP. I'll connect you to {1}'s office now. Please hold on.".format(conversation.first_name, conversation.riding.representative_name))
    answer.pause(length=1)

    if settings.TESTING_PHONE:
      to = settings.TESTING_PHONE
    else:
      to = phonecall.to_number
    answer.dial(to,
                action="{0}{1}".format(settings.SITE_URL, reverse('phone_twilio_completed')),
                callerId=phonecall.from_number,
                ringTone='us')

  else:
    answer.say("Sorry, I wasn't able to complete your call. Please try again.")

  return HttpResponse(str(answer))

# twilio callback when the call completes and the MP hangs up
@csrf_exempt
def twilio_completed(request):
  answer = twiml.Response()
  phonecall = PhoneCall.objects.filter(call_id=request.POST.get('CallSid')).first()

  if phonecall:
    phonecall.completed2 = timezone.now()
    phonecall.call_status2 = request.POST.get('DialCallStatus')
    phonecall.duration2 = request.POST.get('DialCallDuration')
    phonecall.call2_id = request.POST.get('DialCallSid')
    phonecall.save()


  if request.POST.get('DialCallStatus') == 'completed':
    answer.pause(length=2)
    answer.say("Call completed. Thank you, you're awesome.")
  else:
    answer.say("Sorry, I wasn't able to complete your call. Please try again.")

  return HttpResponse(str(answer))

# twilio callback when the call completes and the user hangs up
@csrf_exempt
def twilio_completed2(request):
  phonecall = PhoneCall.objects.filter(call_id=request.POST.get('CallSid')).first()

  if phonecall:
    phonecall.completed = timezone.now()
    phonecall.call_status = request.POST.get('CallStatus')
    phonecall.duration = request.POST.get('CallDuration')
    phonecall.save()
    
    conversation = phonecall.conversation
    conversation.send_sms("Thanks for calling your MP. You're awesome! It's been a pleasure helping you, and I hope we meet again soon.")
    conversation.status = 'c'
    conversation.save()
    

  return HttpResponse("")


