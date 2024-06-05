import datetime
import decimal
from rest_framework import serializers
from .models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'drug_name', 'description', 'price', 'image', 'created_at', 'quantity', 'category', 'manufacturer_country', 'manufacturer', 'active_substance', 'type', 'dozens', 'expiration_date', 'brand', 'seller')
        extra_kwargs = {
            'id': {'read_only': True},
            'drug_name': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'image': {'required': True},
            'created_at': {'read_only': True},
            'quantity': {'required': True},
            'category': {'required': True},
            'manufacturer_country': {'required': True},
            'manufacturer': {'required': True},
            'active_substance': {'required': True},
            'type': {'required': False},
            'dozens': {'required': True},
            'expiration_date': {'required': True},
            'brand': {'required': False},
            'seller': {'read_only': True},
        }

    def validate_expiration_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("Expiration date must be greater than today.")
        return value
    

    def validate_price(self, value):
        if not isinstance(value, decimal.Decimal):
            raise serializers.ValidationError("Price must be a number.")
        if value < 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    

    def validate_image(self, value):
        IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
        IMAGE_MAX_SIZE = 5242880
        if not value.name.endswith(tuple(IMAGE_FILE_TYPES)):
            raise serializers.ValidationError("Image must be a PNG, JPG, or JPEG file.")
        if value.size > IMAGE_MAX_SIZE:
            raise serializers.ValidationError("Image must be less than 5MB.")
        return value
    
    
    def validate_quantity(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Quantity must be an integer.")
        if value < 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    

    def validate_dozens(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Dozens must be an integer.")
        if value < 0:
            raise serializers.ValidationError("Dozens must be greater than 0.")
        return value
    

    def validate_manufacturer_country(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Manufacturer country must contain only letters.")
        return value   
    

    def validate_manufacturer(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Manufacturer must contain only letters.")
        return value

    def validate_category(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Category must contain only letters.")
        return value


    def create(self, validated_data):
        drug = Drug.objects.create(**validated_data)
        return drug

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class DrugUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'drug_name', 'description', 'price', 'image', 'quantity', 'category', 'manufacturer_country', 'manufacturer', 'active_substance', 'type', 'dozens', 'expiration_date', 'brand', 'seller')
        extra_kwargs = {
            'drug_name': {'required': False},
            'description': {'required': False},
            'price': {'required': False},
            'image': {'required': False},
            'quantity': {'required': False},
            'manufacturer_country': {'required': False},
            'manufacturer': {'required': False},
            'active_substance': {'required': False},
            'type': {'required': False},
            'dozens': {'required': False},
            'expiration_date': {'required': False},
            'brand': {'required': False},
            'category': {'required': False},
            'seller': {'read_only': True},
        }

    def validate_price(self, value):
        if not isinstance(value, decimal.Decimal):
            raise serializers.ValidationError("Price must be a number.")
        if value < 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    

    def validate_image(self, value):
        IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
        IMAGE_MAX_SIZE = 5242880
        if not value.drug_name.endswith(tuple(IMAGE_FILE_TYPES)):
            raise serializers.ValidationError("Image must be a PNG, JPG, or JPEG file.")
        if value.size > IMAGE_MAX_SIZE:
            raise serializers.ValidationError("Image must be less than 5MB.")
        return value
    

    def validate_quantity(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Quantity must be an integer.")
        if value < 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    

    def validate_dozens(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Dozens must be an integer.")
        if value < 0:
            raise serializers.ValidationError("Dozens must be greater than 0.")
        return value
    

    def validate_manufacturer_country(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Manufacturer country must contain only letters.")
        return value
    

    def validate_manufacturer(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Manufacturer must contain only letters.")
        return value
    

    def validate_expiration_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("Expiration date must be greater than today.")
        return value
    

    def validate_category(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Category must contain only letters.")
        return value

    def validate_seller(self, value):
        if not value.role == 'seller':
            raise serializers.ValidationError("Seller must be a seller.")
        return value
    

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance