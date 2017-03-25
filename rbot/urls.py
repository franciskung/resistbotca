from django.conf.urls import url
from rbot import views

urlpatterns = [
    url(r'^$', views.handle_sms, name='handle_sms'),
]
