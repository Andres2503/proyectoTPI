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
    path('marcasusuario',views.MarcaListaPorUsuarioLogueado.as_view()),
    path('userdetalle', views.DetalleUsuario.as_view()), 
    path('productocreate',views.ProductoCrear.as_view()),
    path('productoagregarlista',views.AgregarProductoLista.as_view()),
    path('productodetail/<int:pk>',views.ProductoDetalle.as_view()),
    path('productos',views.ProductosLista.as_view()),
    path('verlistadeseos',views.VerListaDeseos.as_view()),
    path('categoriacreate',views.AgregarCategoria.as_view()),
    path('categoriadetail/<int:pk>',views.VerCategoria.as_view()),
    path('ordencreate',views.AgregarOrden.as_view()),
    path('verorden/<int:pk>',views.VerOrden.as_view()),
    path('lineaordencreate',views.AgregarLineaOrden.as_view()),
    path('verlineaorden/<int:pk>',views.VerLineaOrden.as_view()),
    path('pagocreate',views.AgregarPago.as_view()),
    path('verpago/<int:pk>',views.VerPago.as_view()),
    path('calificacioncreate',views.AgregarCalificacion.as_view()),
    path('vercalificacion/<int:pk>',views.VerCalificacion.as_view()),

    path('productoscategoria',views.VerProductosPorCategoria.as_view()),
    path('productosmarca',views.VerProductosPorMarca.as_view()),
    path('marcasuserprofile',views.VerMarcasPorUserProfile.as_view()),

]