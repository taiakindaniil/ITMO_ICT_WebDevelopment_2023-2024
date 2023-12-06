from django.db import models

# Create your models here.
class CarOwner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True)


class DriverLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type_id = models.CharField(max_length=10)
    issue_date = models.DateTimeField()
    

class Car(models.Model):
    number = models.CharField(max_length=15)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    owners = models.ManyToManyField(CarOwner, through="CarOwnership")

    def __str__(self) -> str:
        return self.model.capitalize()


class CarOwnership(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)