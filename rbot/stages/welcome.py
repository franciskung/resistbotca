class Welcome:
  name = 'welcome'

  def get_messages(self):
    return ["Hello!"]
  
  def respond(self, conversation, message):
    return (self, "You said {0} from {1}".format(message, conversation.phone_number))

