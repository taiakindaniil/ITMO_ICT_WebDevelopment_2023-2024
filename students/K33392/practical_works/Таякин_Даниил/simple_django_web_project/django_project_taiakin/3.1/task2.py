from project_first_app.models import *

tesla_cars = Car.objects.filter(model="Tesla")

for car in tesla_cars:
    print(f"Car Number: {car.number}")
    print(f"Model: {car.model}")
    print(f"Color: {car.color}")
    print("--------------------")


michael_drivers = CarOwner.objects.filter(first_name="Michael")
for driver in michael_drivers:
    print(f"Driver Name: {driver.first_name}")
    print(f"Date of Birth: {driver.birth_date}")
    print("--------------------")


driver = CarOwner.objects.get(first_name="Sarah")
print(f"Driver Name: {driver.first_name}")
print(f"Date of Birth: {driver.birth_date}")
print("--------------------")

driver_licenses = DriverLicense.objects.filter(owner=driver)
for license in driver_licenses:
    print(f"License Number: {license.number}")
    print(f"License Type: {license.type_id}")
    print(f"Issue Date: {license.issue_date}")
    print("--------------------")


red_cars = Car.objects.filter(color="Red")
for car in red_cars:
    print(f"Car Number: {car.number}")
    print(f"Model: {car.model}")
    print(f"Color: {car.color}")
    print("--------------------")


target_year = 2023
owners_with_cars_from_year = CarOwner.objects.filter(
    carownership__start_date__year=target_year
).distinct()

for owner in owners_with_cars_from_year:
    print(f"Owner Name: {owner.first_name}")
    print(f"Date of Birth: {owner.birth_date}")
    print("--------------------")