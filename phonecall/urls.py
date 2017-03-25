from django.conf.urls import url
from phonecall import views

urlpatterns = [
    url(r'^twilio_incoming/$', views.twilio, name='phone_twilio'),
    url(r'^twilio_completed/$', views.twilio_completed, name='phone_twilio_completed'),
    url(r'^twilio_completed2/$', views.twilio_completed2, name='phone_twilio_completed2'),
]
