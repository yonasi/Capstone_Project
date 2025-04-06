from rest_framework import permissions
from django.contrib.auth.models import User


class IsAssignedUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.assigned_to == request.user
    


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_staff
    


class IsAssignedOrReadOnly(permissions.BasePermission):
    
    #Allows read access to anyone, but only assigned users or managers can update or delete.
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.assigned_to == request.user or request.user.is_manager

class IsCompanyAdminOrReadOnly(permissions.BasePermission):

    #Allows read access to anyone, but only staff users can create, update, or delete companies.
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class CanAssignContact(permissions.BasePermission):
    
    #Allows users to assign contacts to themselves or managers to assign to others.
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            assigned_to_id = request.data.get('assigned_to')
            if assigned_to_id:
                try:
                    assigned_user = User.objects.get(pk=assigned_to_id)
                    return request.user == assigned_user or request.user.is_manager
                except User.DoesNotExist:
                    return False
            return True  
        return True

class IsManagerOrReadOnly(permissions.BasePermission):
    
    #Allows read access to anyone, but only managers can perform write operations.

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_manager