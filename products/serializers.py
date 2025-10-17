from rest_framework import serializers
from .models import Category, Product


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


class ProductSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ('id' ,'name', 'description', 'price', 'discount_price', 'stock', 'created_at', 'updated_at', 'category')
        read_only_fields = ['id', 'created_at', 'updated_at', ]

    def validate(self, attrs):
        name = attrs.get('name')
        category = attrs.get('category')
        if attrs.get('discount_price'):
            discount = attrs.get('discount_price')
            if discount > attrs.get('price'):
                raise serializers.ValidationError('The discount must be less than the product price.')
        if category.product_set.filter(name=name).exists(): # or Product.objects.filter(name=name, category=category)
            raise serializers.ValidationError('name is exist')

        return attrs



