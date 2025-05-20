from rest_framework import permissions

class IsEmailVerified(permissions.BasePermission):
    """
    Allows access only to users with verified email.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Check if user has a profile and is_verified is True
        if hasattr(user, 'profile') and getattr(user.profile, 'is_verified', False):
            return True
        return False

class IsUserTypeVerified(permissions.BasePermission):
    """
    Allows access only to users with verified user_type (second-step verification).
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Check if user_type is set and user_type_verified is True
        if hasattr(user, 'profile'):
            profile = user.profile
            if profile.user_type and profile.user_type_verified:
                return True
        return False

class IsSuperUserOrUserTypeVerified(permissions.BasePermission):
    """
    Allows access to superusers or users with verified user_type.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        return IsUserTypeVerified().has_permission(request, view)