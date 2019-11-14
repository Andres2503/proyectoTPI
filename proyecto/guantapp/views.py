from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics

from guantapp.models import User, Marca
from guantapp.serializers import UserSerializer, MarcaSerializer

from rest_framework import permissions
from guantapp.permissions import IsOwnerOrReadOnlyUser, IsOwnerOrReadOnlyMarca


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.AllowAny]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnlyUser]

class MarcaList(generics.ListAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MarcaCreate(generics.CreateAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile_id=self.request.user.id)

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MarcaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnlyMarca]

