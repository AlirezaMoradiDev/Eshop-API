from rest_framework import serializers
from .models import Category


class CategorySerializers(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), required=False, allow_null=True)  #to read and write the parent field by object name instead of ID

    class Meta:
        model = Category
        fields = ('name', 'image', 'description', 'id', 'parent')
        read_only_fields = ['id', ]

    def validate_parent(self, value):
        if Category.objects.filter(name=value).exists():
            return value
        else:
            raise serializers.ValidationError("There is no category!")