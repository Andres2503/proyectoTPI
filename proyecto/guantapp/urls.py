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
    path('productocreate',views.ProductoCrear.as_view()),
    path('productoagregarlista',views.AgregarProductoLista.as_view()),
    path('productodetail/<int:pk>',views.ProductoDetalle.as_view()),
    path('productos',views.ProductosLista.as_view()),
    path('verlistadeseo',views.VerListaDeseos.as_view()),
    path('categoriacreate',views.AgregarCategoria.as_view()),
    path('categoriadetail/<int:pk>',views.VerCategoria.as_view()),    
]