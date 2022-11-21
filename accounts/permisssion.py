from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if obj.created_by == request.user:
                return True
            else:
                return False
        else:
            return True
