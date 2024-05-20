import factory
from tracker.models import Category, Transaction, User
from datetime import datetime, timedelta


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: f'user{n}')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Iterator(
        [
            'Bills',
            'Housing',
            'Salary',
            'Food',
            'Social',
        ]
    )


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = 5
    date = factory.Faker(
        'date_between',
        start_date=(datetime.now() - timedelta(days=365)).date(),
        end_date=datetime.now().date(),
    )
    type = factory.Iterator(
        [type[0] for type in Transaction.TypeChoices.choices],
    )
