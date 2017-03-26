from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from emailfax.models import WrittenMessage

class Stage:
  name = 'email_send'

  def get_messages(self, conversation):
    return []

  # sends the actual email! whoa!
  def do_action(self, conversation, response):
    msg = WrittenMessage.objects.filter(conversation=conversation).first()
    
    if msg:
      if settings.TESTING_EMAIL:
        to = settings.TESTING_EMAIL
      else:
        to = conversation.riding.representative_email
    
      send_mail(msg.topic,
                msg.build_body(),
                u"\"{0}\" <{1}>".format(conversation.raw_name, conversation.email),
                [to,],
                fail_silently=False)

    # and cleanup
    conversation.send_sms("Thanks for emailing your MP. You're awesome! It's been a pleasure helping you, and I hope we meet again soon.")
    conversation.status = 'c'
    conversation.save()
  
  def respond(self, conversation, message):
    # we are done. nothing left.
    #return (None, None)
    
    from rbot.stages import email_preview
    return (email_preview.Stage(), None)
    
