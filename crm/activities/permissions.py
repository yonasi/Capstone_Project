from rest_framework import permissions
from django.contrib.auth.models import User

class IsContactRelatedOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.created_by == request.user or obj.contact.assigned_to == request.user
    

class IsContactRelatedOrReadOnly(permissions.BasePermission):

   # Allows read access to anyone, but only users related to the contact
    #(creator, assigned user of contact, or manager) can modify activities.
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user or obj.contact.assigned_to == request.user or request.user.is_manager

class CanAssignActivity(permissions.BasePermission):
    
    #Allows users to assign activities to themselves or managers to assign to others.

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            assigned_to_id = request.data.get('assigned_to')
            if assigned_to_id:
                try:
                    assigned_user = User.objects.get(pk=assigned_to_id)
                    return request.user == assigned_user or request.user.is_manager
                except User.DoesNotExist:
                    return False
            return True  # Allow other updates
        return True

class CanExtendDueDate(permissions.BasePermission):

    #Allows managers to extend the due date of activities.

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            if 'due_date' in request.data:
                return request.user.is_manager
        return True # Allow other updatesS