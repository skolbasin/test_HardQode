from rest_framework import permissions
from .models import ProductAccess


class HasProductAccess(permissions.BasePermission):
    message = "You dont have access to this product"

    def has_permission(self, request, view):
        return ProductAccess.objects.filter(
            product_id=view.kwargs.get("id"), user=request.user
        ).exists()
