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
      conversation.contact_method = 'phone'
      conversation.save()
      
      from rbot.stages import phone
      return (phone.Stage(), None)

    elif 'email' in command or 'e-mail' in command:
      conversation.contact_method = 'email'
      conversation.save()
      
      if conversation.email:
        from rbot.stages import email_topic
        return (email_topic.Stage(), None)
      else:
        from rbot.stages import email
        return (email.Stage(), None)

    
    elif 'fax' in command:
      """
      conversation.contact_method = 'phone'
      conversation.save()
      
      from rbot.stages import fax
      return (fax.Stage(), None)
      """
      pass


    # error      
    self.error = True
    return (self, u"I wish I could help you {0}, but I haven't learned that yet. Try a phone call or email?".format(command))
      

