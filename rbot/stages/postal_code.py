import re

from ridings.lookup import postal_code_lookup

class Stage:
  name = 'postal_code'

  def get_messages(self, conversation):
    return [u"Hi, {0}. Can you also tell me your postal code so I can find your MP?".format(conversation.first_name)]
  
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
      
      from rbot.stages import contact_topic
      return (contact_topic.Stage(), u"Great, I found your MP: {0} ({1}, {2})".format(riding.representative_name, riding.representative_party, riding.riding_name))

    # if the lookup failed, prompt them to retry              
    else:
      from rbot.stages import postal_code_failed
      return (postal_code_failed.Stage(), None)

