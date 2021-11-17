from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Project, Contributor, Issue, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'author', 'title', 'description', 'p_type')
        read_only_fields = ['id', 'author']

class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ('id', 'project_id', 'user', 'role', 'permission')
        read_only_fields = ['id', 'project_id']

class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ('id','project_id','title', 'description', 'author', 'created_time','attributed', 'priority', 'tag', 'status')
        read_only_fields = ['id', 'project_id', 'author', 'created_time']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'issue', 'author', 'description', 'created_time')
        read_only_fields = ('id', 'issue', 'author', 'created_time')