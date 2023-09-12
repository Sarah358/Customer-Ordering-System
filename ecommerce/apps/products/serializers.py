from rest_framework import serializers

from .models import Category, Product


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for product categories
    """

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading products
    """

    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for writing products
    """

    slug = serializers.SlugField(read_only=True)

    category = ProductCategoryReadSerializer()

    class Meta:
        model = Product
        fields = (
            'slug',
            'category',
            'name',
            'description',
            'image',
            'price',
            'stock',
        )

    def validate_price(self, value):
        """
        Custom field-level validation for 'price'.
        """
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        """
        Custom field-level validation for 'stock'.
        """
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        instance, created = Category.objects.get_or_create(**category)
        product = Product.objects.create(**validated_data, category=instance)

        return product

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            nested_serializer = self.fields['category']
            nested_instance = instance.category
            nested_data = validated_data.pop('category')
            nested_serializer.update(nested_instance, nested_data)

        return super(ProductWriteSerializer, self).update(instance, validated_data)
