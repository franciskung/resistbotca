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
      return (contact_topic.Stage(), u"Great, I found your MP: {0} ({1})".format(riding.representative_name, riding.riding_name))
              
    # if the lookup failed, retry this stage
    else:
      return (self, None)

