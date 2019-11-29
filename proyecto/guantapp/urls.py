from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from rest_framework import routers
from guantapp import views

urlpatterns = [    
    #Relacionado a usuario
    path('userlist', views.UserLista.as_view()),
    path('usercreate', views.UserCrear.as_view()),
    path('userdetail/<int:pk>', views.UserDetalle.as_view()),    
    path('userdetalle', views.DetalleUsuario.as_view()), 

    #Relacionado a marca
    path('marcacreate', views.MarcaCrear.as_view()),
    path('marcalist', views.MarcaLista.as_view()),
    path('marcadetail/<int:pk>', views.MarcaDetalle.as_view()),
    path('marcasusuario',views.MarcaListaPorUsuarioLogueado.as_view()),
    path('marcasuserprofile',views.VerMarcasPorUserProfile.as_view()),

    #Relacionado a producto    
    path('productocreate',views.ProductoCrear.as_view()),    
    path('productodetail/<int:pk>',views.ProductoDetalle.as_view()),
    path('productos',views.ProductosLista.as_view()),
    path('productoscategoria',views.VerProductosPorCategoria.as_view()),
    path('productosmarca',views.VerProductosPorMarca.as_view()),    

    #Relacionado a lista deseos
    path('verlistadeseos',views.VerListaDeseos.as_view()),
    path('productoagregarlista',views.AgregarProductoLista.as_view()),

    #Relacionado a categoria
    path('categoriacreate',views.AgregarCategoria.as_view()),
    path('categoriadetail/<int:pk>',views.VerCategoria.as_view()),
    path('hijoscategoria',views.VerHijosDeCategoria.as_view()),

    #Relacionado a orden
    path('ordencreate',views.AgregarOrden.as_view()),
    path('ordendetail/<int:pk>',views.VerOrden.as_view()),

    #Relacionado a linea orden
    path('lineaordencreate',views.AgregarLineaOrden.as_view()),
    path('lineaordendetail/<int:pk>',views.VerLineaOrden.as_view()),

    #Relacionado a pago
    path('pagocreate',views.AgregarPago.as_view()),
    path('pagodetail/<int:pk>',views.VerPago.as_view()),

    #Relacionado a calificacion
    path('calificacioncreate',views.AgregarCalificacion.as_view()),
    path('calificaciondetail/<int:pk>',views.VerCalificacion.as_view()),
    path('vercalificacionesproducto',views.VerCalificacionesProducto.as_view()),
            
]