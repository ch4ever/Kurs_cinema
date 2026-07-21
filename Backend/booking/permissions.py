from rest_framework.permissions import BasePermission

class isOwnerOrAdminOfTicket(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role =="ADMIN":
            return True
        return obj.user_id == user.id