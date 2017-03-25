from emailfax.models import WrittenMessage

class Stage:
  name = 'email_body'

  def get_messages(self, conversation):
    return ["Great, I'll use that as a subject line. And now please write your message (I'll add your name at the bottom for you)"]
  
  def respond(self, conversation, message):
    msg, created = WrittenMessage.objects.get_or_create(conversation=conversation)
    msg.message = message
    msg.save()
    
    # advance to next stage    
    from rbot.stages import email_preview
    return (email_preview.Stage(), None)

