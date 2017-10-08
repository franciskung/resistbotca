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

