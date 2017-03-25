from django.conf.urls import url
from emailfax import views

urlpatterns = [
    url(r'^get_mms/(?P<message_id>[0-9]+)/$', views.get_mms, name='emailfax_mms'),
]
