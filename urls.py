__author__ = 'AnishKannan'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^results/$', views.results, name='results'),
    ]
    #url(r'^results(?P<classes>.*)/$', views.results, name='results'),
