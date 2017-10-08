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


from django.db import models

import PIL
from io import BytesIO
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from rbot.models import Conversation
from ridings.models import PostalCode

class WrittenMessage(models.Model):
  conversation = models.ForeignKey(Conversation)
  sent = models.DateTimeField(blank=True, null=True)
  
  message = models.TextField(blank=True, null=True)

  png = models.BinaryField(blank=True, null=True)

  # topic is DEPRECATED! only kept for backwards-compatibilty; now using Conversation.topic
  topic = models.CharField(max_length=255, blank=True, null=True)
  
  def build_body(self):
    pcode = PostalCode.objects.filter(postal_code=self.conversation.postal_code).first()
    
    body = u"""Dear {0},

I live in your riding of {1}, and I am writing to you today about {2}.

{3}

Thank you for your attention.

{4}
{5}
{6}, {7}
{8}
""".format(self.conversation.riding.representative_name,
           self.conversation.riding.riding_name,
           self.conversation.topic,
           self.message,
           self.conversation.get_name(),
           self.conversation.postal_code,
           pcode.city if pcode else "",
           self.conversation.riding.province,
           self.conversation.phone_number)
           
    return body
  
  
  def generate_png(self):
    # set up the image
    color = "#000"
    bgcolor = "#fff"
    fontsize = 20
    leftpadding = 3
    rightpadding = 3
    width = 800
    REPLACEMENT_CHARACTER = u'\uFFFD'
    NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '  

    try:
      font = ImageFont.truetype("opensans.ttf", fontsize)
    except:
      font = ImageFont.load_default()

    # set up the template and merge text    
    text = self.build_body()
    
    # ok, the rest is basically magic from https://gist.github.com/destan/5540702
    text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)
    lines = []
    line = u""
    
    for word in text.split():
      #print word
      
      if word == REPLACEMENT_CHARACTER: #give a blank line
        lines.append( line[1:] ) #slice the white space in the begining of the line
        line = u""
        #lines.append( u"" ) #the blank line
      elif font.getsize( line + ' ' + word )[0] <= (width - rightpadding - leftpadding):
        line += ' ' + word
      else: #start a new line
        lines.append( line[1:] )
        line = u""
        
        #TODO: handle too long words at this point
        line += ' ' + word #for now, assume no word alone can exceed the line width

    if len(line) != 0:
      lines.append( line[1:] ) #add the last line

    line_height = font.getsize(text)[1] + 2
    img_height = line_height * (len(lines) + 1)
    
    img = Image.new("RGBA", (width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)
    
    y = 0
    for line in lines:
      draw.text( (leftpadding, y), line, color, font=font)
      y += line_height
      
    io_buffer = BytesIO()
    img.save(io_buffer, "png")
    
    self.png = io_buffer.getvalue()
    io_buffer.close()
    
    self.save()

