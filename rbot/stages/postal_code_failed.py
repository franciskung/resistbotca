import re

from rbot.stages.postal_code import PostalCode
from ridings.lookup import postal_code_lookup

class PostalCodeFailed:
  name = 'postal_code_failed'

  def get_messages(self, conversation):
    return ["hmm, I wasn't able to find that postal code. Can you try again?"]
  
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
      
      return (PostalCode(), u"Your MP is {0}, in {1}".format(riding.representative_name, riding.riding_name))
              
    # if the lookup failed, retry this stage
    else:
      return (self, None)

