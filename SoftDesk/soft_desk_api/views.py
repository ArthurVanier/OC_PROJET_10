from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
import requests
from django.contrib.auth.models import User
from .models import Contributor, Issue, Project, Comment
from .serializers import CommentSerializer, UserSerializer, ProjectSerializer, ContributorSerializer, IssuesSerializer
from .permissions import CommentPermission, ContributorPermission, ProjectPermission, IssuesPermission


class Login(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid:
            username = serializer.data['username']
            password = serializer.data['password']
            return Response(self.get_jwt_token(username, password), status=status.HTTP_200_OK)
        return Response("Invalid data provided", status=status.HTTP_400_BAD_REQUEST)
    
    def get_jwt_token(username, password):
        data = {"username": username, "password": password}
        res = requests.post('http://127.0.0.1:8000/jwt/get_token/', data=data).json()
        return res


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
                return Response("Account Created", status=status.HTTP_200_OK)
        return Response("Invalid data provided", status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

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
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response("Invalid data provided", status=status.HTTP_400_BAD_REQUEST)


class ContributorsViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [IsAuthenticated, ContributorPermission]

    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs['projects_pk'])

    def create(self, request, projects_pk):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=projects_pk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Invalid data provided", status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, projects_pk, pk):
        contributor = get_object_or_404(Contributor, project_id=projects_pk, user=pk)
        if contributor:
            contributor.delete()
            return Response(status=status.HTTP_200_OK)
        return Response("Invalid data provided", status=status.HTTP_400_BAD_REQUEST)


class IssuesViewSet(viewsets.ModelViewSet):
    serializer_class = IssuesSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated, IssuesPermission]

    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs['projects_pk'])

    def create(self, request, projects_pk):
        serializer = IssuesSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print('serializer valid')
            project = get_object_or_404(Project, pk=projects_pk)
            attributed = get_object_or_404(User, pk=serializer.validated_data['attributed'].id)
            serializer.save(project_id=project, attributed=attributed, author=request.user, created_time=datetime.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Invalid data provided", status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, CommentPermission]

    def get_queryset(self):
        return self.queryset.filter(issue=self.kwargs['issues_pk'])
    
    def create(self, request, projects_pk, issues_pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            issue = get_object_or_404(Issue, pk=issues_pk)
            serializer.save(author=request.user, created_time=datetime.now(), issue=issue)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Invalid data provided", status=status.HTTP_400_BAD_REQUEST)
