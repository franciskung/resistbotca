class Stage:
  name = 'contact_topic'
  returning = False
  no_easter_eggs = True

  def get_messages(self, conversation):
    if self.returning:
      return [u"It's great to see you again! What topic do you want to discuss with {0} today?".format(conversation.riding.representative_name)]
    else:
      return [u"And what topic do you want to discuss with {0} today?".format(conversation.riding.representative_name)]

  def respond(self, conversation, message):
    conversation.topic = message
    conversation.save()

    from rbot.stages import contact_method
    return (contact_method.Stage(), None)

