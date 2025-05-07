from rest_framework import permissions

class IsSuperUserOrUserTypeBased(permissions.BasePermission):
    """
    Custom permission to allow superusers and users with specific user_type to access their profile.
    """
    def has_permission(self, request, view):
        # Allow access to superusers
        if request.user.is_superuser:
            return True

        # Allow access to authenticated users with user types
        if hasattr(request.user, 'profile'):
            # Ensure user has a profile and check their user_type
            if request.user.profile.user_type in ['user', 'brand', 'influencer']:
                return True
        
        return False
