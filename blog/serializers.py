import os
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import PostModel, Comment

User = get_user_model()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = [
            "title",
            "content",
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

class UpdateSerialzation(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = [
            "title",
            "content",


        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "content",
        ]
class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "body",
        ]
