import re

from ridings.lookup import postal_code_lookup

class PostalCode:
  name = b'postal_code'

  def get_messages(self, conversation):
    return [u"It's great to meet you, {0}. Next, can you give me your postal code so I can look up your MP?".format(conversation.first_name)]
  
  def respond(self, conversation, message):
    # clean up postal code
    pcode = re.sub('[^0-9A-Z]', '', message.upper())
    
    # look it up
    riding = postal_code_lookup(pcode)
    
    # if it worked out, save to the Conversation object, report out, and advance to next stage
    if riding:
      conversation.postal_code = pcode
      conversation.representative = 'mp'
      conversation.riding = riding
      conversation.save()
      
      return (self, u"Your MP is {0}, in {1}".format(riding.representative_name, riding.riding_name))

    # if the lookup failed, prompt them to retry              
    else:
      from rbot.stages.postal_code_failed import PostalCodeFailed
      return (PostalCodeFailed(), None)

