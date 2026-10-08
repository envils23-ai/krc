
from .models import ClientAddress
from django.forms import ModelForm

# Создание пользователя с сайта
class ClientAddressCreationForm(ModelForm):
    class Meta:
        model = ClientAddress
        fields = ['client_adress_region',
                  'client_adress_city',
                  'client_adress_street',
                  'client_adress_building_number',
                  'client_adress_phone_number',
                  ]







