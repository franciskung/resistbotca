from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404

from emailfax.models import WrittenMessage

# this is a pretty bad case of security-by-obscurity where people can see others' messages...
# gotta find a way of fixing this later. add some kind of hash/etc to the url maybe?
def get_mms(request, message_id):
  msg = WrittenMessage.objects.filter(id=message_id).first()
  
  if msg:
    return HttpResponse(msg.png, content_type='image/png')
  
  else:
    return Http404("not found")
