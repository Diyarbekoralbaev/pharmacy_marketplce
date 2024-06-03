from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'address', 'email', 'phone', 'date_joined', 'role')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address': {'required': True},
            'email': {'required': False},
            'phone': {'required': True},
            'role': {'required': True},
            'date_joined': {'read_only': True},
        }

    def validate(self, data):
        if self.instance:
            # On update, avoid validating unique fields that belong to the current instance
            if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=data['username']).exists():
                raise serializers.ValidationError('This username is already taken.')
            if CustomUser.objects.exclude(pk=self.instance.pk).filter(phone=data['phone']).exists():
                raise serializers.ValidationError('This phone number is already taken.')
            if data.get('email') and CustomUser.objects.exclude(pk=self.instance.pk).filter(email=data['email']).exists():
                raise serializers.ValidationError('This email is already taken.')
        else:
            # On creation, ensure unique fields are not already taken
            if CustomUser.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('This username is already taken.')
            if CustomUser.objects.filter(phone=data['phone']).exists():
                raise serializers.ValidationError('This phone number is already taken.')
            if data.get('email') and CustomUser.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('This email is already taken.')

        if data['role'] not in dict(CustomUser.ROLE_CHOICES):
            raise serializers.ValidationError('This role is not valid.')

        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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
