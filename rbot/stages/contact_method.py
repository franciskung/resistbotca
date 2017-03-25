from __future__ import unicode_literals
import re

from ridings.lookup import postal_code_lookup

class PostalCode:
  name = 'postal_code'

  def get_messages(self, conversation):
    return ["hmm, I wasn't able to find that postal code. Can you try again?"]
  
  def respond(self, conversation, message):
    # clean up postal code
    pcode = re.sub('[^0-9A-Z]', '', message.upper())
    
    # look it up
    riding = postal_code_lookup(pcode)
    
    if riding:
      conversation.postal_code = pcode
      conversation.representative = 'mp'
      conversation.riding = riding
      conversation.save()
      
      return (self, "Your MP is {0}, in {1}".format(riding.representative_name, riding.riding_name))
              
    else:
      return (self, None)

