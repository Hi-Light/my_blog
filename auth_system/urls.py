from django.conf.urls import url, include
from auth_system.views import *

urlpatterns = [url(r'^is_exist$', is_exist, name='is_exist'),
               url(r'^login$', login, name='login'),
               url(r'^logout$', logout_user, name='logout')]
