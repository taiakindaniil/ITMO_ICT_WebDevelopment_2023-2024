from datetime import datetime, timedelta
from django.utils import timezone
from project_first_app.models import *

# Create 7 car owners
owners_data = [
    {
        "first_name": "Michael",
        "last_name": "Johnson",
    },
    {
        "first_name": "Sarah",
        "last_name": "Williams",
    },
    {
        "first_name": "David",
        "last_name": "Brown",
    },
    {
        "first_name": "Emily",
        "last_name": "Davis",
    },
    {
        "first_name": "Matthew",
        "last_name": "Robinson",
    },
    {
        "first_name": "Olivia",
        "last_name": "Martinez",
    },
]

owners = [CarOwner.objects.create(**data) for data in owners_data]


# Create 6 cars
cars_data = [
    {"number": "PQR789", "model": "Audi", "color": "Black"},
    {"number": "STU012", "model": "Mercedes", "color": "Red"},
    {"number": "VWX345", "model": "Volkswagen", "color": "Gray"},
    {"number": "YZA678", "model": "Subaru", "color": "Blue"},
    {"number": "BCD901", "model": "Volvo", "color": "Silver"},
    {"number": "EFG234", "model": "Tesla", "color": "White"},
]

for data in cars_data:
    Car.objects.create(**data)


# Create driver's licenses for each owner
licenses_data = [
    {
        "owner": owner,
        "number": f"DL{index + 1}",
        "type_id": "A",
        "issue_date": timezone.now(),
    }
    for index, owner in enumerate(owners)
]

for data in licenses_data:
   DriverLicense.objects.create(**data)


# Assign 1 to 3 cars for each owner
for owner, car in zip(CarOwner.objects.all(), Car.objects.all()):
    CarOwnership.objects.create(
        owner=owner,
        car=car,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=365),
    )