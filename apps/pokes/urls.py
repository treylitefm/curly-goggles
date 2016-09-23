from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^poke/(?P<user_id>\d+)', views.poke, name='poke'),
    url(r'^', views.index, name='index'),
]
