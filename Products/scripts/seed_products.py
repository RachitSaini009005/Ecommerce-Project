import os
import django
import random
from faker import Faker
from django.contrib.auth import get_user_model

# ✅ Point Django to correct settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecommerce_Project.settings")
django.setup()

from Products.models import Product  # Import AFTER django.setup()

fake = Faker()
User = get_user_model()
owner = User.objects.first()

categories = ["Electronics", "Fashion", "Books", "Sports", "Home"]

# Add 20 fake products
for _ in range(20):
    Product.objects.create(
        owner=owner,
        name=fake.word().capitalize(),
        price=round(random.uniform(100, 5000), 2),
        description=fake.text(max_nb_chars=100),
        stock=random.randint(1, 50),
        category=random.choice(categories),
    )

print("✅ 20 fake products added!")
