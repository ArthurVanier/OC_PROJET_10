from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
import requests

from .permissions import ContributorPermission, ProjectPermission

from .models import Contributor, Project
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer
from django.contrib.auth.models import User

# Create your views here.

def get_jwt_token(username, password):
    data = {"username": username, "password": password}
    res = requests.post('http://127.0.0.1:8000/jwt/get_token/', data=data).json()
    return res

class Login(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response()

    def post(self, request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid:
            username = serializer.data['username']
            password = serializer.data['password']
            return Response(get_jwt_token(username, password))
        return Response()

class CreateAccount(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response()
    
    def post(self, request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid:
            username = serializer.data['username']
            if User.objects.filter(username=username).count() == 0:
                password = serializer.validate_password(serializer.data['password'])
                User.objects.create(username=username, password=password)
                return Response(data=get_jwt_token(username, password))
        return Response()

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update' or self.action == 'destroy':
            permission_classes.append(ProjectPermission)

        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author=request.user)
            Contributor.objects.create(
                user=request.user,
                project_id=project.id,
                role="Project Manager",
                permission="all"
            )
            return Response(data=serializer.data)
        return Response("error")

class ContributorsViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [IsAuthenticated, ContributorPermission]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['projects_pk'])

    def create(self, request, projects_pk):
        return Response(projects_pk)

