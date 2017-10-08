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
  name = 'email'

  def get_messages(self, conversation):
    return ["I'd love to help you email {0}. But first, what's YOUR email address?".format(conversation.riding.representative_name)]
  
  def respond(self, conversation, message):
    # update conversation object
    # TODO: do some validation for good emails?
    conversation.email = message
    conversation.save()

    # advance to next stage    
    from rbot.stages import email_body
    return (email_body.Stage(), None)

