from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from rest_framework import routers
from guantapp import views


urlpatterns = [    
    path('userlist', views.UserList.as_view()),
    path('usercreate', views.UserCreate.as_view()),
    path('userdetail/<int:pk>', views.UserDetail.as_view()),
    path('marcacreate', views.MarcaCreate.as_view()),
    path('marcalist', views.MarcaList.as_view()),
    path('marcadetail/<int:pk>', views.MarcaDetail.as_view()),
]