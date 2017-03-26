from nameparser import HumanName

class Stage:
  name = 'welcome'

  def get_messages(self, conversation):
    return ["Hi! I'm the Canadian ResistBot, and I'm here to help you contact your Member of Parliament. First off, what's your name?"]
  
  def respond(self, conversation, message):
    # parse name
    name = HumanName(message)
    name.capitalize(force=True)
    
    if name.middle:
      first_name = "{0} {1}".format(name.first, name.middle)
    else:
      first_name = name.first
    last_name = name.last
    
    # update conversation object
    conversation.raw_name = message
    conversation.first_name = first_name
    conversation.last_name = last_name
    conversation.save()

    # advance to next stage    
    from rbot.stages import postal_code
    return (postal_code.Stage(), None)

