from emailfax.models import WrittenMessage

class Stage:
  name = 'email_body'
  no_easter_eggs = True

  def get_messages(self, conversation):
    return [u"Great, I'll use that as a subject line. And what do you want to say to {0}? (I'll add your name at the end of the message, too)".format(conversation.riding.representative_name)]
  
  def respond(self, conversation, message):
    msg, created = WrittenMessage.objects.get_or_create(conversation=conversation)
    msg.message = message
    msg.save()
    
    # advance to next stage    
    from rbot.stages import email_preview
    return (email_preview.Stage(), None)

