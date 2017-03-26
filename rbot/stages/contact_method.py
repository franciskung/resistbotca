class Stage:
  name = 'contact_method'
  error = False

  def get_messages(self, conversation):
    if not self.error:
      return [u"Now, how would you like to contact your MP, {0}? Phone, email, or fax?".format(conversation.riding.representative_name)]
    else:
      return []
  
  def respond(self, conversation, message):
    # clean up command
    command = message.lower().strip()

    # delegate based on action
    if 'phone' in command:
      from rbot.stages import phone
      return (phone.Stage(), None)

    elif 'email' in command or 'e-mail' in command:
      if conversation.email:
        from rbot.stages import email_topic
        return (email_topic.Stage(), None)
      else:
        from rbot.stages import email
        return (email.Stage(), None)

    
    elif 'fax' in command:
      """
      from rbot.stages import phone, email, fax
      elif command == 'email' or command == 'e-mail':
        return (email.Stage(), None)
      elif command == 'fax':
        return (fax.Stage(), None)
      """

      return (self, u"I wish I could help you {0}, but I haven't learned that yet. Try a phone call or email?".format(command))


    # error      
    self.error = True
    return (self, "Sorry, I didn't understand that. Can you reply with phone, email, or fax?")
      

