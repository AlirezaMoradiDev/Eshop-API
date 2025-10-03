from rest_framework import serializers
from .models import Category


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'image', 'description', 'id')
        read_only_fields = ['id', ]
