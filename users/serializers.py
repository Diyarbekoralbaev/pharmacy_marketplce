from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'address', 'email', 'phone', 'date_joined', 'role', 'password')
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
            'password': {'write_only': True},
        }

    def validate(self, data):
        if self.instance:
            if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=data['username']).exists():
                raise serializers.ValidationError('This username is already taken.')
            if CustomUser.objects.exclude(pk=self.instance.pk).filter(phone=data['phone']).exists():
                raise serializers.ValidationError('This phone number is already taken.')
            if data.get('email') and CustomUser.objects.exclude(pk=self.instance.pk).filter(email=data['email']).exists():
                raise serializers.ValidationError('This email is already taken.')
        else:
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError('Incorrect credentials')


class UserChangeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'address', 'email', 'phone')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address': {'required': True},
            'email': {'required': False},
            'phone': {'required': True},
        }

    def validate(self, data):
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(phone=data['phone']).exists():
            raise serializers.ValidationError('This phone number is already taken.')
        if data.get('email') and CustomUser.objects.exclude(pk=self.instance.pk).filter(email=data['email']).exists():
            raise serializers.ValidationError('This email is already taken.')
        if 'role' in data:
            raise serializers.ValidationError('You cannot change your role.')
        if 'username' in data:
            raise serializers.ValidationError('You cannot change your username.')
        if 'password' in data:
            raise serializers.ValidationError('You cannot change your password.')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError('Old password is incorrect.')
        if data.get('old_password') == data.get('new_password'):
            raise serializers.ValidationError('New password should be different from the old password.')
        return data


class UserForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()


class UserResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp_code = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        otp_code = data.get('otp_code')
        password = data.get('password')
        if not phone or not otp_code or not password:
            raise serializers.ValidationError('Phone, OTP code, and password are required.')
        if not CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('User not found.')
        return data
