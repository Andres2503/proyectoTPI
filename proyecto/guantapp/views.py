from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from guantapp.models import User, UserProfile, Marca, Producto, ListaDeseos, Categoria, Calificacion, Orden, Pago, LineaOrden
from guantapp.serializers import UserSerializer, MarcaSerializer, MarcaReadSerializer, ProductoSerializer, ProductoReadSerializer,ListaDeseosSerializer, ListaDeseosReadSerializer, PagoSerializer, LineaOrdenSerializer, OrdenSerializer, CalificacionSerializer, CalificacionReadSerializer, LineaOrdenReadSerializer, CategoriaSerializer, CategoriaReadSerializer, PagoReadSerializer, OrdenReadSerializer, CalificacionesProductoSerializer
from guantapp.permissions import IsOwnerUser, IsOwnerOrReadOnlyMarca, IsOwnerOrReadOnlyProducto, IsOwnerPagoAndLineaOrden, IsOwnerOrden
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


class MarcaCrear(generics.CreateAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):        
        user_profile=UserProfile.objects.get(user_id=self.request.user.id)
        serializer.save(user_profile_id=user_profile.id)

#View para detalle de marca    
class MarcaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaReadSerializer
        
    permission_classes = [IsOwnerOrReadOnlyMarca]

#View para ver marcas por perfil de usuario
class VerMarcasPorUserProfile(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #serializer_class = MarcaReadSerializer
    serializer_class = MarcaSerializer

    def get_queryset(self):        

        queryset=[]    
        user_profile_id = self.request.query_params.get('user_profile_id', None)
        if user_profile_id is not None:
            queryset=Marca.objects.all().filter(user_profile_id=user_profile_id)        
        return queryset


#View para listar las marcas del usuario logueado por el token
class MarcaListaPorUsuarioLogueado(APIView):            
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):                        
        marcas = Marca.objects.all().filter(user_profile_id=self.request.user.id)
        serializer = MarcaReadSerializer(marcas, many=True)
        return Response(serializer.data)


###################  PRODUCTO #################

class ProductoCrear(generics.CreateAPIView):    
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductoDetalle(generics.RetrieveUpdateDestroyAPIView):    
    queryset = Producto.objects.all()
    serializer_class = ProductoReadSerializer    
    permission_classes = [IsOwnerOrReadOnlyProducto]

#View que lista todos los productos
class ProductosLista(generics.ListAPIView):
    queryset = Producto.objects.all()
    #serializer_class = ProductoSerializer    
    serializer_class = ProductoReadSerializer        
    permission_classes = [permissions.AllowAny]


## Recupera los productos de la categoría
#Si la categoría tiene hijos también recupera sus productos
class VerProductosPorCategoria(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    #serializer_class = ProductoReadSerializer
    serializer_class = ProductoSerializer

    def get_queryset(self):        

        queryset=[]    
        categoria_id = self.request.query_params.get('categoria', None)        
        if categoria_id is not None:
                lista_categorias=Categoria.objects.get(id=categoria_id).get_descendants(include_self=True)
                for categoria in lista_categorias:
                    queryset+=Producto.objects.all().filter(categoria_id=categoria.id)
        else:
            queryset=Producto.objects.all()
        return queryset


#View que lista todos los productos que pertenecen a una marca
class VerProductosPorMarca(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    #serializer_class = ProductoReadSerializer
    serializer_class = ProductoSerializer

    def get_queryset(self):        

        queryset=[]    
        marca_id = self.request.query_params.get('marca', None)
        if marca_id is not None:
            queryset=Producto.objects.all().filter(marca_id=marca_id)        
        return queryset


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
    permission_classes = [IsOwnerPagoAndLineaOrden]


############# ORDEN ############
class AgregarOrden(generics.CreateAPIView):
    serializer_class=OrdenSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_profile=UserProfile.objects.get(user_id=self.request.user.id)        
        serializer.save(comprador=user_profile)

class VerOrden(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orden.objects.all()
    serializer_class = OrdenReadSerializer
    permission_classes = [IsOwnerOrden]


############# LINEA ORDEN ############
class AgregarLineaOrden(generics.CreateAPIView):
    serializer_class = LineaOrdenSerializer
    permission_classes = [permissions.IsAuthenticated]

class VerLineaOrden(generics.RetrieveUpdateDestroyAPIView):
    queryset = LineaOrden.objects.all()
    serializer_class = LineaOrdenReadSerializer
    permission_classes = [IsOwnerPagoAndLineaOrden]


########## CATEGORIA ########
class AgregarCategoria(generics.CreateAPIView):
    serializer_class = CategoriaSerializer
    #permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.IsAuthenticated]

class VerCategoria(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaReadSerializer
    permission_classes = [permissions.AllowAny]


class VerHijosDeCategoria(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    #serializer_class = CategoriaReadSerializer
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        queryset=[]    
        categoria_id = self.request.query_params.get('categoria', None)        
        if categoria_id is not None:            
                #queryset=Categoria.objects.get(id=categoria_id).get_descendants(include_self=True)#Incluye al padre
                queryset=Categoria.objects.get(id=categoria_id).get_descendants(include_self=False)#no incluye al padre
        return queryset

########## CALIFICACION ########
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


class VerCalificacionesProducto(generics.ListAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionesProductoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset=[]    
        producto_id = self.request.query_params.get('producto', None)        
        if producto_id is not None:                            
                queryset=Calificacion.objects.all().filter(producto_id=producto_id)
        return queryset