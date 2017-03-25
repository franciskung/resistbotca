from emailfax.models import WrittenMessage

class Stage:
  name = 'email_preview'

  def get_messages(self, conversation):
    return ["This is looking fantastic - we're nearly there. Reply with PREVIEW to preview your message, or SEND to send it now!"]
  
  def respond(self, conversation, message):
    message = message.lower()
    if "preview" in message:
      # advance to next stage    
      from rbot.stages import email_preview2
      return (email_preview2.Stage(), None)
      
    elif "send" in message:
      # advance to next stage    
      from rbot.stages import email_send
      return (email_send.Stage(), None)

    else:
      # error      
      self.error = True
      return (self, "Sorry, I didn't understand that. Can you reply with PREVIEW or SEND ?")

