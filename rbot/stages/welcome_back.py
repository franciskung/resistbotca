from nameparser import HumanName

class Stage:
  name = 'welcome_back'

  def get_messages(self, conversation):
    from rbot.models import Conversation
    past_conversation = Conversation.objects.filter(phone_number=conversation.phone_number).exclude(id=conversation.id).order_by('-started').first()

    # assume past_conversation is not null, as this stage shouldn't get called if it is.
    # can we do some better error-checking...??
    
    conversation.raw_name = past_conversation.raw_name
    conversation.first_name = past_conversation.first_name
    conversation.last_name = past_conversation.last_name
    conversation.email = past_conversation.email
    conversation.postal_code = past_conversation.postal_code
    conversation.riding = past_conversation.riding
    conversation.representative = past_conversation.representative
    conversation.save()
    
    return [u"Hi ... I remember you! Welcome back! You're {0}, right?".format(past_conversation.get_name())]

  
  def respond(self, conversation, message):
    message = message.lower()
    if 'yes' in message or 'yep' in message or 'yeah' in message or 'right' in message:

      if not conversation.riding:      
        # advance to next stage    
        from rbot.stages import postal_code
        return (postal_code.Stage(), None)

      # advance to next stage
      from rbot.stages import contact_topic
      stage = contact_topic.Stage()
      stage.returning =True
      return (stage, None)
      
    else:
      # clear saved contact info
      conversation.raw_name = None
      conversation.first_name = None
      conversation.last_name = None
      conversation.email = None
      conversation.postal_code = None
      conversation.riding = None
      conversation.representative = None
      conversation.save()
    
      # restart by asking their name
      from rbot.stages import welcome
      return (welcome.Stage(), "Oops. I get people mixed up once in a while - sorry about that!")

