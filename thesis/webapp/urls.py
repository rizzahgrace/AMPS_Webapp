from django.conf.urls import url

from . import views

app_name = 'webapp'
urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^home', views.home, name='home'),
    url(r'^csv', views.csv, name='csv'),
    url(r'^weather', views.weather, name='weather'),
    url(r'^power', views.power, name='power'),
    url(r'^dbbar', views.AdvancedGraph.as_view(), name='dbbar'),
    url(r'^powbar', views.PowerGraph.as_view(), name='powbar'),
]