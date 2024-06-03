from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'address', 'email', 'phone', 'photo', 'date_joined', 'role')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address': {'required': True},
            'email': {'required': False},
            'phone': {'required': True},
            'role': {'required': True},
            'photo': {'required': False},
            'date_joined': {'read_only': True},
        }

    def validate(self, data):
        if self.instance:
            return data
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('This username is already taken.')
        if CustomUser.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError('This phone number is already taken.')
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('This email is already taken.')
        if CustomUser.objects.filter(role=data['role']) not in CustomUser.ROLE_CHOICES:
            raise serializers.ValidationError('This role is not valid.')
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                'username': user.username,
                'role': user.role,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError('Incorrect credentials')
