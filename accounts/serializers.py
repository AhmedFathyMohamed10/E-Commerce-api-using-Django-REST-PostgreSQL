import re #FOR MAKING MATCH IN PASSWORD
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Validate username
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username is already taken."})

        # Validate the email
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use.")

        # Validate password
        password = data.get('password')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise serializers.ValidationError({"password": "Password must contain at least 8 characters, including an uppercase letter, a lowercase letter, a number, and a special character."})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")