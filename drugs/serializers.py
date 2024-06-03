import decimal
from rest_framework import serializers
from .models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'name', 'description', 'price', 'image')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'image': {'required': True},
        }

    def validate(self, data):
        if 'price' in data:
            price = data['price']
            if not isinstance(price, decimal.Decimal):
                raise serializers.ValidationError("Price must be a number.")
            if price < 0:
                raise serializers.ValidationError("Price must be greater than 0.")
        else:
            raise serializers.ValidationError("Price is required.")
        
        IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
        IMAGE_MAX_SIZE = 5242880

        if 'image' in data:
            image = data['image']
            if not image.name.endswith(tuple(IMAGE_FILE_TYPES)):
                raise serializers.ValidationError("Image must be a PNG, JPG, or JPEG file.")
            if image.size > IMAGE_MAX_SIZE:
                raise serializers.ValidationError("Image must be less than 5MB.")
        else:
            raise serializers.ValidationError("Image is required.")
        
        return data


    def create(self, validated_data):
        drug = Drug.objects.create(**validated_data)
        return drug

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance