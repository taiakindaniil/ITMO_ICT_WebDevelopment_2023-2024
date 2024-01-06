# Практическая работа #3.1

## Задание #1
*Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей.*

Для начала создадим 6 владельцев автомобилей. Для создания объекта в базе данных воспользуемся методом `CarOwner.objects.create`. Данные сохранены в списке `owners_data`.

```python
# Create 6 car owners
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
```

Теперь создадим автомобили и присвоим их каждому владельцу соответственно.

```python
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
```

```python
# Assign 1 to 3 cars for each owner
for owner, car in zip(CarOwner.objects.all(), Car.objects.all()):
    CarOwnership.objects.create(
        owner=owner,
        car=car,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=365),
    )
```

Создадим права для вождения для каждого владельца автомобиля.

```python
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
```

Весь написанный скрипт выполняем данной командой:
```sh
python3 manage.py shell < 3.1/task1.py
```


## Задание #2

*По созданным в пр.1 данным написать следующие запросы на фильтрацию:*

- *Где это необходимо, добавьте related_name к полям модели*
- *Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)*
- *Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)*
- *Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)*
- *Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)*
- *Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе)*

Для получения всех автомобилей марки Tesla воспользуемся методом `Car.objects.filter`.

```python
tesla_cars = Car.objects.filter(model="Tesla")

for car in tesla_cars:
    print(f"Car Number: {car.number}")
    print(f"Model: {car.model}")
    print(f"Color: {car.color}")
    print("--------------------")
```

Для поиска водителей с именем "Michael" воспользуемся методом `CarOwner.objects.filter`.

```python
michael_drivers = CarOwner.objects.filter(first_name="Michael")
for driver in michael_drivers:
    print(f"Driver Name: {driver.first_name}")
    print(f"Date of Birth: {driver.birth_date}")
    print("--------------------")
```

Для фильтрации прав по владельцу выполним два запроса при помощи методов `CarOwner.objects.get` и `DriverLicense.objects.filter`.

```python
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
```

Для получения всех красных машин воспользуемся методом `Car.objects.filter`.

```python
red_cars = Car.objects.filter(color="Red")
for car in red_cars:
    print(f"Car Number: {car.number}")
    print(f"Model: {car.model}")
    print(f"Color: {car.color}")
    print("--------------------")
```

Для получения всех владельцев, которые владеют автомобилем начиная с 2023 года воспользуемся методом `CarOwner.objects.filter`.

```python
target_year = 2023
owners_with_cars_from_year = CarOwner.objects.filter(
    carownership__start_date__year=target_year
).distinct()

for owner in owners_with_cars_from_year:
    print(f"Owner Name: {owner.first_name}")
    print(f"Date of Birth: {owner.birth_date}")
    print("--------------------")
```


## Задание #3

*Необходимо реализовать следующие запросы c применением описанных методов:*

- *Вывод даты выдачи самого старшего водительского удостоверения*
- *Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе*
- *Выведите количество машин для каждого водителя*
- *Подсчитайте количество машин каждой марки*
- *Отсортируйте всех автовладельцев по дате выдачи удостоверения (Примечание: чтобы не выводить несколько раз одни и те же таблицы воспользуйтесь методом .distinct()*

Вывод даты выдачи самого старого водительского удостоверения.

```python
oldest_license = DriverLicense.objects.order_by("issue_date").first()
print(f"License Number: {oldest_license.number}")
```

Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе.

```python
oldest_ownership = CarOwnership.objects.order_by("start_date").first()
print(f"Oldest ownership: {oldest_ownership.start_date}")
```

Выведите количество машин для каждого водителя.

```python
owners_with_car_count = CarOwner.objects.annotate(car_count=Count("carownership"))
for owner in owners_with_car_count:
    print(f"Owner Name: {owner.first_name}")
    print(f"Number of cars: {owner.car_count}")
    print("--------------------")
```

Подсчитайте количество машин каждой марки.

```python
cars_by_model = Car.objects.values("model").annotate(car_count=Count("carownership"))
for car in cars_by_model:
    print(f"Car Model: {car['model']}")
    print(f"Number of cars: {car['car_count']}")
    print("--------------------")
```

Отсортируйте всех автовладельцев по дате выдачи удостоверения.

```python
owners_by_license_issue_date = CarOwner.objects.order_by("driverlicense__issue_date")
for owner in owners_by_license_issue_date:
    print(f"Owner Name: {owner.first_name}")
    print("--------------------")
```