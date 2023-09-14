import pytest

from ecommerce.apps.products.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)

from ..factories import CategoryFactory, ProductFactory


@pytest.mark.django_db
def test_product_category_read_serializer():
    category = CategoryFactory(name="Test Category")
    serializer = ProductCategoryReadSerializer(instance=category)
    assert serializer.data['slug'] == category.slug


@pytest.mark.django_db
def test_product_read_serializer():
    category = CategoryFactory(name="Test Category")
    product = ProductFactory(name="Test Product", category=category)
    serializer = ProductReadSerializer(instance=product)
    assert serializer.data['category'] == category.name


@pytest.mark.django_db
def test_product_write_serializer_valid_data():
    # category = CategoryFactory(name="Test Category")
    serializer = ProductWriteSerializer(
        data={
            'name': 'Test Product',
            'description': 'Product description',
            'image': None,
            'price': 10.99,
            'stock': 100,
            'category': {'name': 'Test Category'},  # Uses the factory-generated category data
        }
    )

    assert serializer.is_valid()
    product = serializer.save()
    assert product.name == 'Test Product'
    assert product.category.name == 'Test Category'


@pytest.mark.django_db
def test_product_write_serializer_negative_price():
    # category = CategoryFactory(name="Test Category")
    serializer = ProductWriteSerializer(
        data={
            'name': 'Test Product',
            'description': 'Product description',
            'image': None,
            'price': -10.99,  # Negative price should trigger validation error
            'stock': 100,
            'category': {'name': 'Test Category'},  # Use the factory-generated category data
        }
    )

    assert not serializer.is_valid()


@pytest.mark.django_db
def test_product_write_serializer_negative_stock():
    # category = CategoryFactory(name="Test Category")
    serializer = ProductWriteSerializer(
        data={
            'name': 'Test Product',
            'description': 'Product description',
            'image': None,
            'price': 10.99,
            'stock': -100,  # Negative stock should trigger validation error
            'category': {'name': 'Test Category'},  # Use the factory-generated category data
        }
    )

    assert not serializer.is_valid()
