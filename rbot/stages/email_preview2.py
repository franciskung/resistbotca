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
from emailfax.models import WrittenMessage

class Stage:
  name = 'email_preview2'
  error = False

  def get_messages(self, conversation):
    return ["OK, I'll get a preview ready. It might take a moment, thanks for your patience."]

  def do_action(self, conversation, response):
    if not self.error:
      msg = WrittenMessage.objects.filter(conversation=conversation).first()
      
      if msg:
        msg.generate_png()
        conversation.send_sms("Here's a preview of your message. What do you think? Respond with SEND to send it, or EDIT to re-do it.",
                              response,
                              media_url="{0}{1}".format(settings.SITE_URL, reverse('emailfax_mms', kwargs={'message_id': msg.id})),)
    
  
  def respond(self, conversation, message):
    message = message.lower()
    if "send" in message:
      # advance to next stage    
      from rbot.stages import email_send
      return (email_send.Stage(), None)
      
    elif "edit" in message:
      # advance to next stage    
      from rbot.stages import contact_topic
      return (contact_topic.Stage(), None)

    else:
      # error      
      self.error = True
      return (self, "Sorry, I didn't understand that. Can you reply with SEND or EDIT ?")

