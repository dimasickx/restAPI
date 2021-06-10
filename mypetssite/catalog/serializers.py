from rest_framework import serializers

from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    photo = serializers.SlugRelatedField(many=True, read_only=True, slug_field='get_image_url')

    class Meta:
        model = Pet
        fields = ['id', 'name', 'age', 'type', 'photo', 'created_at']
