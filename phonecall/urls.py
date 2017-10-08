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


from django.conf.urls import url
from phonecall import views

urlpatterns = [
    url(r'^twilio_incoming/$', views.twilio, name='phone_twilio'),
    url(r'^twilio_completed/$', views.twilio_completed, name='phone_twilio_completed'),
    url(r'^twilio_completed2/$', views.twilio_completed2, name='phone_twilio_completed2'),
]
