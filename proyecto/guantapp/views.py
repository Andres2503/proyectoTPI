from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from guantapp.models import User, Marca
from guantapp.serializers import UserSerializer, MarcaSerializer
#from guantapp.serializers import UserSerializer, MarcaSerializer, ProductoSerializer
from guantapp.permissions import IsOwnerUser, IsOwnerOrReadOnlyMarca
from rest_framework import permissions
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

#Creo que no iría, o puede agregarse un permissions.IsAdmin
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


#Creo que no iría, o puede agregarse un permissions.IsAdmin
#Se listan todas las marcas registradas
class MarcaLista(generics.ListAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer    
    permission_classes = [permissions.IsAuthenticated]



#Se listan todas las marcas registradas
#Otra manera, realmente solo se necesita el GET
"""class MarcaLista(APIView):
            
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        permission_classes = [permissions.IsAuthenticated]
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
    serializer_class = MarcaSerializer
        
    permission_classes = [IsOwnerOrReadOnlyMarca]

#View para listar las marcas del usuario del token
class MarcaListaPorUsuario(APIView):            
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):                        
        marcas = Marca.objects.all().filter(user_profile_id=self.request.user.id)
        serializer = MarcaSerializer(marcas, many=True)
        return Response(serializer.data)


#View para crear producto
"""class ProductoCrear(generics.CreateAPIView):    
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]"""


