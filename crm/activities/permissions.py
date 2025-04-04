from rest_framework import permissions


class IsContactRelatedOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.created_by == request.user or obj.contact.assigned_to == request.user