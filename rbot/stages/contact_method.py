import re

class Stage:
  name = 'contact_method'
  error = False

  def get_messages(self, conversation):
    if not self.error:
      return ["Now, how would you like to contact them? Phone, email, or fax?"]
    else:
      return []
  
  def respond(self, conversation, message):
    # clean up command
    command = message.lower().strip()

    # delegate based on action
    if command in ('phone', 'fax', 'email', 'e-mail'):
      return (self, u"You're pretty awesome yourself. And while I wish I could {0}, I haven't learned that yet.".format(command))

      """
      from rbot.stages import phone, email, fax
      if command == 'phone':
        return (phone.Stage(), None)
      elif command == 'email' or command == 'e-mail':
        return (email.Stage(), None)
      elif command == 'fax':
        return (fax.Stage(), None)
      """

    # error      
    self.error = True
    return (self, "Sorry, I didn't understand that. Can you reply with phone, email, or fax?")
      

