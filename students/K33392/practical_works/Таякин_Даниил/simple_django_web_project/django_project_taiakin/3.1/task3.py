from project_first_app.models import *
from django.db.models import Count

# query the oldest drivers license
oldest_license = DriverLicense.objects.order_by("issue_date").first()
print(f"License Number: {oldest_license.number}")


# query the oldest ownership date
oldest_ownership = CarOwnership.objects.order_by("start_date").first()
print(f"Oldest ownership: {oldest_ownership.start_date}")


# query the number of cars for each driver using Count annotate
owners_with_car_count = CarOwner.objects.annotate(car_count=Count("carownership"))
for owner in owners_with_car_count:
    print(f"Owner Name: {owner.first_name}")
    print(f"Number of cars: {owner.car_count}")
    print("--------------------")


# query number of cars by model
cars_by_model = Car.objects.values("model").annotate(car_count=Count("carownership"))
for car in cars_by_model:
    print(f"Car Model: {car['model']}")
    print(f"Number of cars: {car['car_count']}")
    print("--------------------")


# query all car owners sorted by drivers license issue date
owners_by_license_issue_date = CarOwner.objects.order_by("driverlicense__issue_date")
for owner in owners_by_license_issue_date:
    print(f"Owner Name: {owner.first_name}")
    print("--------------------")