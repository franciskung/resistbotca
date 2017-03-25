import thread
from phonecall.views import start_call

class Stage:
  name = 'phone'

  def get_messages(self, conversation):
    return [u"I'd love to help you speak with {0}. I'll call your phone in a few seconds, and then connect you to their office.".format(conversation.riding.representative_name)]


  # places the actual phone call
  # conversation is the parent conversation object; response is the TwiML response object
  def do_action(self, conversation, response):
    #success = start_call(conversation)
    thread.start_new_thread(start_call, (conversation,))
    

  def respond(self, conversation, message):
    # there is nothing to respond to for this action.
    return (None, None)

    #from rbot.stages import contact_method
    #return (contact_method.Stage(), None)

