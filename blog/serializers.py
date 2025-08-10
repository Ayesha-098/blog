# blog/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Tag, User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created', 'active']

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'publish_date', 'status', 'tags']

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
