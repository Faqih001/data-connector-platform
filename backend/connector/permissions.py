from rest_framework.permissions import BasePermission
from rest_framework import status
from .models import StoredFile


class IsAdminOrReadOnly(BasePermission):
    """
    Allow admins full access, users can only read.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsFileOwnerOrAdmin(BasePermission):
    """
    Allow access only to admins or the file owner.
    """
    message = '❌ Access denied. You can only access files you own or files shared with you.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin has full access
        if request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return True
        
        # Owner has full access
        if obj.user == request.user:
            return True
        
        # User can read shared files
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return obj.shared_with.filter(id=request.user.id).exists()
        
        return False


class IsFileOwnerOrAdminForWrite(BasePermission):
    """
    Allow write operations only to admins or the file owner.
    """
    message = '❌ You can only modify files you own.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin can modify all files
        if request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return True
        
        # Only owner can modify
        return obj.user == request.user


class IsAdminUserOrOwner(BasePermission):
    """
    Combined permission for both admins and file owners.
    """
    message = '❌ Permission denied. Admin or owner access required.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin')
        is_owner = obj.user == request.user
        return is_admin or is_owner
