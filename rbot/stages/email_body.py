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


from emailfax.models import WrittenMessage

class Stage:
  name = 'email_body'
  no_easter_eggs = True

  def get_messages(self, conversation):
    return [u"Great. And what do you want to say to {0}? (I'll add your name at the end of the message, too)".format(conversation.riding.representative_name)]
  
  def respond(self, conversation, message):
    msg, created = WrittenMessage.objects.get_or_create(conversation=conversation)
    msg.message = message
    msg.save()
    
    # advance to next stage    
    from rbot.stages import email_preview
    return (email_preview.Stage(), None)

