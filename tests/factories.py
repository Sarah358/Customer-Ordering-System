import factory
from django.db.models.signals import post_save
from django.utils.text import slugify
from factory import fuzzy
from faker import Factory as FakeFactory

from ecommerce.apps.orders.models import Order, OrderItem
from ecommerce.apps.products.models import Category, Product
from ecommerce.apps.profiles.models import Profile
from ecommerce.settings.base import AUTH_USER_MODEL

faker = FakeFactory.create()


# profile factory
@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("tests.factories.UserFactory")
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    profile_photo = factory.LazyAttribute(lambda x: faker.file_extension(category="image"))
    city = factory.LazyAttribute(lambda x: faker.city())
    address = factory.LazyAttribute(lambda x: faker.address())

    class Meta:
        model = Profile


# user factory
@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    username = factory.LazyAttribute(lambda x: faker.first_name())
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    class Meta:
        model = AUTH_USER_MODEL

    # controls whether to create a normal user or a super user
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


# products and categories factories
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda x: faker.word())


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda x: faker.paragraph())
    price = factory.Faker('random_number', digits=2, fix_len=True)
    category = factory.SubFactory(CategoryFactory)
    image = factory.django.ImageField(color='red')
    stock = factory.Faker('random_int', min=1, max=100)
    created_at = factory.Faker('date_time_this_decade', tzinfo=None)
    updated_at = factory.Faker('date_time_this_decade', tzinfo=None)

    # Automatically generate unique slugs based on the name
    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    buyer = factory.SubFactory(UserFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = fuzzy.FuzzyInteger(1, 10)
