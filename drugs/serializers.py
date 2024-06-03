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
    
    def create(self, validated_data):
        drug = Drug.objects.create(**validated_data)
        return drug

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance