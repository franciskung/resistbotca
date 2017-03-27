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

