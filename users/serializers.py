from django.shortcuts import render
from rest_framework import serializers
from users.models import User,ProfileModel
from django.contrib.auth.models import User

class userRegistrationSerialization(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User

        fields = ['username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return super(userRegistrationSerialization, self).create(validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.CharField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'username']