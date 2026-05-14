from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import defaultUser


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        if not data['username'] or not data['password']:
            raise ValidationError('Username or password is required')
        return data

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,max_length=150 ,write_only=True)

    def validate(self, data):
        nickname = data.get('username')
        pas = data.get("password")
        if defaultUser.objects.filter(username=nickname).exists():
            raise ValidationError("User with this username already exists")

        if len(nickname) < 3 or len(pas) < 3:
            raise ValidationError("Password or Username must be at least 3 characters long")
        return data

    def create(self, validated_data):
        user = defaultUser.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = defaultUser
        fields = ('id', 'username','role')