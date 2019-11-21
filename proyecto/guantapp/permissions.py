from rest_framework import permissions

class IsOwnerUser(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #Queremos que solo el propio usuario pueda acceder a sus datos, por tanto eliminamos
        #if request.method in permissions.SAFE_METHODS:
            #return True
        
        return obj.profile.user ==request.user        

class IsOwnerOrReadOnlyMarca(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #Permitimos que otros usuarios puedan acceder a leer los datos de la marca de otro usuario
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner 
        return obj.user_profile.user ==request.user        