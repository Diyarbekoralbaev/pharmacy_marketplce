from django.contrib.auth import authenticate
from rest_framework import serializers

from drugs.serializers import DrugSerializer
from .models import CustomUser, OrderModel, OrderItemModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'business_name', 'address', 'email', 'phone', 'date_joined', 'role', 'password')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'business_name': {'required': False},
            'address': {'required': True},
            'email': {'required': False},
            'phone': {'required': True},
            'role': {'required': True},
            'date_joined': {'read_only': True},
            'password': {'write_only': True},
        }

    def validate_role(self, value):
        if value not in dict(CustomUser.ROLE_CHOICES):
            raise serializers.ValidationError('This role is not valid.')
        return value

    def validate_business_name(self, value):
        role = self.initial_data.get('role')
        if role == 'buyer' and value:
            raise serializers.ValidationError('Buyers cannot have a business drug_name.')
        if role == 'seller' and not value:
            raise serializers.ValidationError('Business drug_name is required for sellers.')
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError('This phone number is already taken.')
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already taken.')
        return value

    def validate(self, data):
        data = super().validate(data)
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

        if not username:
            raise serializers.ValidationError('Username is required.')
        if not password:
            raise serializers.ValidationError('Password is required.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Incorrect credentials.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


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

    def validate_phone(self, value):
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(phone=value).exists():
            raise serializers.ValidationError('This phone number is already taken.')
        return value

    def validate_email(self, value):
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError('This email is already taken.')
        return value

    def validate(self, data):

        if self.instance.role == 'buyer' and 'business_name' in data:
            raise serializers.ValidationError('Buyers cannot add a business drug_name.')

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
        if self.context['request'].user.check_password(data.get('new_password')):
            raise serializers.ValidationError('New password must be different from the old password.')


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


class OrderItemSerializer(serializers.ModelSerializer):
    drug_details = DrugSerializer(source='drug', read_only=True)
    class Meta:
        model = OrderItemModel
        fields = ('id', 'drug', 'quantity', 'price', 'drug_details')
        extra_kwargs = {
            'id': {'read_only': True},
            'drug': {'required': True},
            'quantity': {'required': True},
            'price': {'required': True},
            'drug_details': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ('id', 'user', 'created_at', 'status', 'total_price', 'items')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'status': {'required': False},
            'total_price': {'read_only': True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = OrderModel.objects.create(**validated_data)
        total_price = 0
        for item_data in items_data:
            OrderItemModel.objects.create(order=order, **item_data)
            cache_key = f'drug-{item_data["drug"].id}'
            cache.delete(cache_key)
            total_price += item_data['price']
        order.total_price = total_price
        order.save()
        cache.delete('drugs')
        return order
