from django.forms import ModelForm
from .models import CarOwner, Car

class CarOwnerForm(ModelForm):
    
    class Meta:
        model = CarOwner
        fields = [
            "first_name",
            "last_name",
        ]
