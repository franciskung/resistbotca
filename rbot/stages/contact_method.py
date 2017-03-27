# -*- coding: UTF-8 -*-

from emailfax.models import WrittenMessage

class Stage:
  name = 'contact_method'
  error = False
  returning = False

  def get_messages(self, conversation):
    if not self.error:
      return [u"Important stuff. How would you like to send your message? Phone, email, or fax?".format(conversation.riding.representative_name)]
    else:
      return []
  
  def respond(self, conversation, message):
    # clean up command
    command = message.lower().strip()

    # delegate based on action
    if 'phone' in command or 'email' in command or 'e-mail' in command:
      msg, created = WrittenMessage.objects.get_or_create(conversation=conversation)
      msg.save()

    if 'phone' in command:
      conversation.contact_method = 'phone'
      conversation.save()
      
      from rbot.stages import phone
      return (phone.Stage(), None)

    elif 'email' in command or 'e-mail' in command:
      conversation.contact_method = 'email'
      conversation.save()
      
      if conversation.email:
        from rbot.stages import email_body
        return (email_body.Stage(), None)
      else:
        from rbot.stages import email
        return (email.Stage(), None)

    
    elif 'fax' in command:
      conversation.contact_method = 'fax'
      conversation.save()
      
      #from rbot.stages import fax
      #return (fax.Stage(), None)
      from rbot.stages import email_body
      return (email_body.Stage(), None)


    # error      
    self.error = True
    
    if 'pigeon' in command or 'pokemon' in command or u'pokémon' in command:
      return (self, u"You think you're funny, do you? (ok, I think you're funny too.) But seriously. How do you want to contact {0}?".format(conversation.riding.representative_name))
      
    
    return (self, u"I wish I could help you {0}, but I haven't learned that yet. Try a phone call, email, or fax?".format(command))
      

