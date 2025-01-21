from rest_framework import permissions


class ClientDocumentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Superusers can access all documents
        if request.user.is_superuser:
            return True
        
        # Check if the user is associated with the client
        # Add your specific business logic here
        return obj.client.user == request.user