from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from guantapp.models import User, UserProfile, Marca, Producto, ListaDeseos, Categoria, Calificacion, Orden, Pago, LineaOrden
from guantapp.serializers import UserSerializer, MarcaSerializer, MarcaReadSerializer, ProductoSerializer, ProductoReadSerializer,ListaDeseosSerializer, ListaDeseosReadSerializer, PagoSerializer, LineaOrdenSerializer, OrdenSerializer, CalificacionSerializer, CalificacionReadSerializer, LineaOrdenReadSerializer, CategoriaSerializer, CategoriaReadSerializer, PagoReadSerializer, OrdenReadSerializer
from guantapp.permissions import IsOwnerUser, IsOwnerOrReadOnlyMarca, IsOwnerOrReadOnlyProducto
from rest_framework import permissions
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status


################  USER Y USERPROFILE #################

#Creo que no iría, o puede agregarse un permissions.IsAdminUser
#Lista todos los usuarios registrados
class UserLista(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#View para crear usuarios, todos tienen acceso
class UserCrear(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [permissions.AllowAny]    

#View para detalle de usuario, solo los usuarios respectivos pueden acceder a su infomarción
#Se necesita el pk en la url
class UserDetalle(generics.RetrieveUpdateDestroyAPIView):    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [IsOwnerUser]  


#Otra manera para obtener el detalle del usuario sin necesidad del pk en la url
#Busca el detalle por el token enviado
#url: http://127.0.0.1/guantapp/userdetalle  (uso puerto 80)
class DetalleUsuario(APIView):
    permissions_classes=[IsOwnerUser]
    def get(self,request,format=None):
        usuario=User.objects.all().filter(id=self.request.user.id)
        serializer=UserSerializer(usuario,many=True)
        return Response(serializer.data)


################  MARCA #################


#Creo que no iría, o puede agregarse un permissions.IsAdminUser
#Se listan todas las marcas registradas
class MarcaLista(generics.ListAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaReadSerializer    
    permission_classes = [permissions.IsAuthenticated]



#Se listan todas las marcas registradas
#Otra manera, realmente solo se necesita el GET
#########################         MarcaReadSerializer
"""class MarcaLista(APIView):
            
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):        
        marcas = Marca.objects.all()
        serializer = MarcaSerializer(marcas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MarcaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_profile_id=self.request.user.id)            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""


#View para crear marca
class MarcaCrear(generics.CreateAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_profile_id=self.request.user.id)
        #serializer.save(user_id=self.request.user.id)

#View para detalle de marca    
class MarcaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaReadSerializer
        
    permission_classes = [IsOwnerOrReadOnlyMarca]

#View para listar las marcas del usuario del token
class MarcaListaPorUsuario(APIView):            
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):                        
        marcas = Marca.objects.all().filter(user_profile_id=self.request.user.id)
        serializer = MarcaReadSerializer(marcas, many=True)
        return Response(serializer.data)


################  PRODUCTO #################

#View para crear producto
class ProductoCrear(generics.CreateAPIView):    
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

#Detalle de producto
class ProductoDetalle(generics.RetrieveUpdateDestroyAPIView):    
    queryset = Producto.objects.all()
    serializer_class = ProductoReadSerializer    
    permission_classes = [IsOwnerOrReadOnlyProducto]

#Lista de todos los productos
class ProductosLista(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoReadSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]
            

################  LISTA DE DESEO #################

#View para agregar producto a la lista de deseo de usuario(solo necesita pk del producto, el id va en el token)
class AgregarProductoLista(generics.CreateAPIView):
    serializer_class=ListaDeseosSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_profile=UserProfile.objects.get(user_id=self.request.user.id)
        serializer.save(user_profile_id=user_profile.id)

#Para recuperar la lista de deseos del usuario
class VerListaDeseos(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):                        
        user_profile=UserProfile.objects.get(user_id=self.request.user.id)
        productos = ListaDeseos.objects.all().filter(user_profile_id=user_profile.id)
        serializer = ListaDeseosReadSerializer(productos, many=True)
        return Response(serializer.data)


############## PAGO ###########
class AgregarPago(generics.CreateAPIView):
    serializer_class=PagoSerializer
    permission_classes=[permissions.IsAuthenticated]

class VerPago(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoReadSerializer
    permission_classes = [permissions.IsAuthenticated]

############# Orden ############
class AgregarOrden(generics.CreateAPIView):
    serializer_class=OrdenSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_profile=UserProfile.objects.get(user_id=self.request.user.id)        
        serializer.save(comprador=user_profile)

class VerOrden(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orden.objects.all()
    serializer_class = OrdenReadSerializer
    permission_classes = [permissions.IsAuthenticated]


############# LineaOrden ############
class AgregarLineaOrden(generics.CreateAPIView):
    serializer_class = LineaOrdenSerializer
    permission_classes = [permissions.IsAuthenticated]

class VerLineaOrden(generics.RetrieveUpdateDestroyAPIView):
    queryset = LineaOrden.objects.all()
    serializer_class = LineaOrdenReadSerializer
    permission_classes = [permissions.IsAuthenticated]

########## Categoria ########
class AgregarCategoria(generics.CreateAPIView):
    serializer_class = CategoriaSerializer
    #permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.IsAuthenticated]

class VerCategoria(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaReadSerializer
    permission_classes = [permissions.AllowAny]



########## Calificacion ########
class AgregarCalificacion(generics.CreateAPIView):
    serializer_class = CalificacionSerializer    
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        user_profile=UserProfile.objects.get(user_id=self.request.user.id)        
        serializer.save(user_profile=user_profile)

class VerCalificacion(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionReadSerializer
    permission_classes = [permissions.AllowAny]


#########################################################
class VerProductosPorCategoria(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductoReadSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Producto.objects.all()
        categoria = self.request.query_params.get('categoria', None)
        if categoria is not None:
            queryset = Producto.objects.all().filter(categoria=categoria)
        return queryset
