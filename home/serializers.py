from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Email is already taken')
        if data['username']:
            if User.objects.filter(email = data['username']).exists():
                raise serializers.ValidationError('username is already taken')
            
            return data
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email = validated_data['email']
            )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FriendshipSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']