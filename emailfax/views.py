"""
ResistbotCA

Copyright (c) 2017 franciskung.com consulting ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. 
"""


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
