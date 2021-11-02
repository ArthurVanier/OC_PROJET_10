from rest_framework import permissions
from .models import Contributor

class ProjectPermission(permissions.BasePermission):

    edit_methods = ('GET', 'PUT', 'DELETE')

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.author == request.user:
            return True
        
        if request.method == 'GET' and Contributor.objects.filter(project_id=obj.id, user=request.user).count() == 1:
            return True
        
        return False

class ContributorPermission(permissions.BasePermission):

    edit_methods = ('GET', 'POST', 'PUT', 'DELETE')
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if Contributor.objects.filter(project_id=view.kwargs.get('projects_pk', 0), user=request.user).count() == 1:
            return True

        return False