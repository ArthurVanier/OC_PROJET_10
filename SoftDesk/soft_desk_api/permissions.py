from django.db.models.query import QuerySet
from rest_framework import permissions
from .models import Contributor, Project


class ProjectPermission(permissions.BasePermission):

    edit_methods = ('GET', 'PUT', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method == 'GET' and Contributor.objects.filter(project_id=view.kwargs.get('pk'), user=request.user).count() == 1:
            return True

        project = Project.objects.filter(pk=view.kwargs.get('pk'))
        if request.method == 'GET' and project.count() == 0:
            return True

        if project.count() == 1:
            if request.user == project[0].author:
                return True

        return False


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

        if request.method == 'DELETE':
            contributor = Contributor.objects.filter(project_id=view.kwargs.get('projects_pk', 0), user=request.user)
            if contributor.count() == 1 and (contributor[0].permission == "all" or contributor[0].permission.contain('delete')):
                return True
            else:
                return False

        if Contributor.objects.filter(project_id=view.kwargs.get('projects_pk', 0), user=request.user).count() == 1:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return True
        else:
            return False


class IssuesPermission(permissions.BasePermission):

    edit_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if Contributor.objects.filter(project_id=view.kwargs.get('projects_pk', 0), user=request.user).count() == 1:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if obj.author == request.user:
                return True
            else:
                return False

        if request.method == 'PUT':
            if obj.author == request.user or obj.attributed == request.user:
                return True
            else:
                return False

        if Contributor.objects.filter(project_id=view.kwargs.get('projects_pk', 0), user=request.user).count() == 1:
            return True

        return False


class CommentPermission(permissions.BasePermission):
    edit_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if Contributor.objects.filter(project_id=view.kwargs.get('projects_pk', 0), user=request.user).count() == 1:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if obj.author == request.user:
                return True
            else:
                return False

        if request.method == 'PUT':
            if obj.author == request.user:
                return True
            else:
                return False

        if Contributor.objects.filter(project_id=view.kwargs.get('projects_pk', 0), user=request.user).count() == 1:
            return True

        return False
