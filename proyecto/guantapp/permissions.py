from rest_framework import permissions

class IsOwnerUser(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #Queremos que solo el propio usuario pueda acceder a sus datos,
        #comentamos el siguiente if: 

        #if request.method in permissions.SAFE_METHODS:
            #return True
        
        return obj.profile.user ==request.user        

class IsOwnerPagoAndLineaOrden(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        return obj.orden.comprador.user==request.user

class IsOwnerOrden(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        return obj.comprador.user==request.user

class IsOwnerOrReadOnlyMarca(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):        
        #Permitimos que otros usuarios puedan acceder a leer los datos de la marca de otro usuario
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #Permisos de escritura solo son permitidos al propietario de la marca
        return obj.user_profile.user ==request.user        

class IsOwnerOrReadOnlyProducto(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        
        #Permitimos que otros usuarios puedan acceder a leer los datos del producto de otro usuario
        if request.method in permissions.SAFE_METHODS:
            return True

        #Permisos de escritura solo son permitidos al propietario de la marca
        return obj.marca.user_profile.user ==request.user        