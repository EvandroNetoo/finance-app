import random
from faker import Faker
from django.core.management import BaseCommand
from tracker.models import User, Transaction, Category


class Command(BaseCommand):
    help = 'Generates transactions for testing'

    def handle(self, *args, **kwargs) -> str | None:
        fake = Faker()

        categories = [
            'Bills',
            'Food',
            'Clothes',
            'Medical',
            'Housing',
            'Salary',
            'Social',
            'Transport',
            'Vacation',
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)

        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(
                username='admin', password='1234'
            )

        categories = Category.objects.all()
        types = [type[0] for type in Transaction.TypeChoices.choices]
        for _ in range(20):
            Transaction.objects.create(
                user=user,
                category=random.choice(categories),
                amount=random.uniform(1, 2500),
                date=fake.date_between(start_date='-1y', end_date='today'),
                type=random.choice(types),
            )
