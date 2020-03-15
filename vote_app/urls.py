from django.urls import path, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('home', views.home),
    path('voting', csrf_exempt(views.voting)),
    re_path(r'index/(?P<activity_id>\d+)$', views.index),
]
