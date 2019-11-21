from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from rest_framework import routers
from guantapp import views


urlpatterns = [    
    path('userlist', views.UserLista.as_view()),
    path('usercreate', views.UserCrear.as_view()),
    path('userdetail/<int:pk>', views.UserDetalle.as_view()),    
    path('marcacreate', views.MarcaCrear.as_view()),
    path('marcalist', views.MarcaLista.as_view()),
    path('marcadetail/<int:pk>', views.MarcaDetalle.as_view()),
    path('marcasusuario',views.MarcaListaPorUsuario.as_view()),
    path('userdetalle', views.DetalleUsuario.as_view()), 
    #path('productocreate',views.ProductoCrear.as_view()),
       

]