from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import PostModel,Comment

User = get_user_model()

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = [
            "title",
            "content",
            "draft",
        ]

class PostListSerializer(serializers.ModelSerializer):


    class Meta:
        model = PostModel
        fields = [
            "id",
            "title",
            "author",
            "content",
            "date_created",

        ]

class PostListSerializer(serializers.ModelSerializer):


    class Meta:
        model = PostModel
        fields = [
            "id",
            "title",
            "author",
            "content",
            "date_created",
            "draft",

        ]

class updatePostSerializer(serializers.ModelSerializer):


    class Meta:
        model = PostModel
        fields = [
            "title",
            "content",
            "draft",
        ]

class updatePostSerializer(serializers.ModelSerializer):


    class Meta:
        model = PostModel
        fields = [
            "title",
            "content",
            "draft",
        ]

class deletePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = [
            "id",
            "title",
            "content",
            "draft",
        ]
class CreatComment(serializers.ModelSerializer):
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "user",
            "post",
            "content",
        ]

    def create(self, validate_data):
     return Comment.objects.create(**validate_data)



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "content",
            "post",
        ]