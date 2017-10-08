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
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from emailfax.models import WrittenMessage

class Stage:
  name = 'email_send'

  def get_messages(self, conversation):
    return []

  # sends the actual email! whoa!
  def do_action(self, conversation, response):
    msg = WrittenMessage.objects.filter(conversation=conversation).first()
    
    if msg:
      if conversation.contact_method == 'fax':
      
        if settings.TESTING_FAX:
          to = settings.TESTING_FAX
        else:
          to = conversation.riding.representative_fax
      
        send_mail(conversation.topic,
                  msg.build_body(),
                  u"\"{0}\" <{1}>".format(conversation.get_name(), settings.FAX_FROM_EMAIL),
                  [u"\"{0}\" <{1}@srfax.com>".format(conversation.riding.representative_name, to),],
                  fail_silently=False)

      else:    
        if settings.TESTING_EMAIL:
          to = settings.TESTING_EMAIL
        else:
          to = conversation.riding.representative_email
      
        send_mail(conversation.topic,
                  msg.build_body(),
                  u"\"{0}\" <{1}>".format(conversation.get_name(), conversation.email),
                  [to,],
                  fail_silently=False)

    # and cleanup
    conversation.send_sms("... and done. That was easy! It's been a pleasure helping you (you're awesome, by the way), and I hope we meet again soon.")
    conversation.status = 'c'
    conversation.save()
  
  def respond(self, conversation, message):
    # we are done. nothing left.
    return (None, None)
    
    #from rbot.stages import email_preview
    #return (email_preview.Stage(), None)

