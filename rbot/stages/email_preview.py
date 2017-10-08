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
  name = 'email_preview'
  error = False

  def get_messages(self, conversation):
    if not self.error:
      return ["This is looking fantastic - we're nearly there. Reply with PREVIEW to preview your message, or SEND to send it now!"]
    else:
      return []
  
  def respond(self, conversation, message):
    message = message.lower()
    if "preview" in message:
      # advance to next stage    
      from rbot.stages import email_preview2
      return (email_preview2.Stage(), None)
      
    elif "send" in message:
      # advance to next stage    
      from rbot.stages import email_send
      return (email_send.Stage(), None)

    else:
      # error      
      self.error = True
      return (self, "Sorry, I didn't understand that. Can you reply with PREVIEW or SEND ?")

