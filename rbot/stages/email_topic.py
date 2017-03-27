from emailfax.models import WrittenMessage

class Stage:
  name = 'email_topic'
  no_easter_eggs = True

  def get_messages(self, conversation):
    return ["OK. And what topic are you writing to {0} about?".format(conversation.riding.representative_name)]
  
  def respond(self, conversation, message):
    msg, created = WrittenMessage.objects.get_or_create(conversation=conversation)
    msg.topic = message
    msg.save()
    
    # advance to next stage    
    from rbot.stages import email_body
    return (email_body.Stage(), None)

