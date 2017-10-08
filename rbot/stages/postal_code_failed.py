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


import re

from ridings.lookup import postal_code_lookup

class Stage:
  name = 'postal_code_failed'

  def get_messages(self, conversation):
    return ["hmm, I wasn't able to find that postal code. Can you double-check it and try again?"]
  
  def respond(self, conversation, message):
    # clean up postal code
    pcode = re.sub('[^0-9A-Z]', '', message.upper())
    
    # look it up
    riding = postal_code_lookup(pcode)

    # if it worked out, save to the Conversation object, report out, and advance to next stage
    # (this block is duplicated in postal_code.py too)
    if riding:
      conversation.postal_code = pcode
      conversation.representative = 'mp'
      conversation.riding = riding
      conversation.save()
      
      from rbot.stages import contact_topic
      return (contact_topic.Stage(), u"Great, I found your MP: {0} ({1}, {2})".format(riding.representative_name, riding.representative_party, riding.riding_name))
              
    # if the lookup failed, retry this stage
    else:
      return (self, None)

