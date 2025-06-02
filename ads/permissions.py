from rest_framework.permissions import BasePermission

class IsBrand(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'brand'

class IsInfluencer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'influencer'

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in ['GET', 'HEAD'] or obj.creator == request.user.userprofile
