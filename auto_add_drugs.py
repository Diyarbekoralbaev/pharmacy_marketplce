import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_marketplce.settings')


django.setup()

from datetime import date
from decimal import Decimal
from users.models import CustomUser
from drugs.models import Drug

seller_instance = CustomUser.objects.get(username='Diyarbek')


Drug.objects.bulk_create([
    Drug(
        drug_name="Aspirin",
        description="Pain reliever and fever reducer.",
        price=Decimal("5.99"),
        image="images/drugs/aspirin.jpg",
        quantity=50,
        expiration_date=date(2025, 12, 31),
        brand="Bayer",
        category="Pain Reliever",
        manufacturer_country="Germany",
        manufacturer="Bayer AG",
        active_substance="Acetylsalicylic Acid",
        type="Tablet",
        dozens=10,
        seller=seller_instance
    ),
    Drug(
        drug_name="Ibuprofen",
        description="Nonsteroidal anti-inflammatory drug.",
        price=Decimal("8.49"),
        image="images/drugs/ibuprofen.jpg",
        quantity=100,
        expiration_date=date(2024, 11, 30),
        brand="Advil",
        category="Anti-inflammatory",
        manufacturer_country="USA",
        manufacturer="Pfizer",
        active_substance="Ibuprofen",
        type="Tablet",
        dozens=20,
        seller=seller_instance
    ),
    Drug(
        drug_name="Amoxicillin",
        description="Antibiotic used to treat bacterial infections.",
        price=Decimal("12.75"),
        image="images/drugs/amoxicillin.jpg",
        quantity=75,
        expiration_date=date(2023, 10, 15),
        brand="Amoxil",
        category="Antibiotic",
        manufacturer_country="UK",
        manufacturer="GlaxoSmithKline",
        active_substance="Amoxicillin",
        type="Capsule",
        dozens=15,
        seller=seller_instance
    ),
    Drug(
        drug_name="Loratadine",
        description="Antihistamine used to treat allergies.",
        price=Decimal("7.50"),
        image="images/drugs/loratadine.jpg",
        quantity=120,
        expiration_date=date(2026, 1, 20),
        brand="Claritin",
        category="Antihistamine",
        manufacturer_country="Belgium",
        manufacturer="Merck & Co.",
        active_substance="Loratadine",
        type="Tablet",
        dozens=12,
        seller=seller_instance
    ),
    Drug(
        drug_name="Metformin",
        description="Medication used to treat type 2 diabetes.",
        price=Decimal("4.20"),
        image="images/drugs/metformin.jpg",
        quantity=200,
        expiration_date=date(2025, 6, 30),
        brand="Glucophage",
        category="Antidiabetic",
        manufacturer_country="France",
        manufacturer="Sanofi",
        active_substance="Metformin",
        type="Tablet",
        dozens=20,
        seller=seller_instance
    ),
])

print("Drugs added successfully!")