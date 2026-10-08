
from .models import Client
from django.forms import ModelForm
from django import forms
from adress.models import ClientAddress
from django.db.models import Q

# Создание пользователя с сайта
class ClientCreationForm(ModelForm):
    class Meta:
        model = Client
        fields = ['client_code',
                  'client_name',
                  'client_registration_region',
                  'client_registration_city',
                  'email',
                  'client_phone_number',
                  ]

class ClientCreationForm(ModelForm):
    addresses = forms.ModelMultipleChoiceField(
        queryset=ClientAddress.objects.none(),
        required=False,
        label='Адреси',
    )

    class Meta:
        model = Client
        fields = ['client_code', 'client_name', 'client_registration_region',
                  'client_registration_city', 'email', 'client_phone_number']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields['addresses']

        # Доступны свободные адреса и адреса этого клиента
        available = Q(client__isnull=True)
        if self.instance.pk:
            available |= Q(client=self.instance)
        field.queryset = ClientAddress.objects.filter(available)

        # В HTML рендерим только выбранные адреса
        if self.is_bound:
            ids = [i for i in self.data.getlist(self.add_prefix('addresses')) if i.isdigit()]
            selected = field.queryset.filter(pk__in=ids)
        elif self.instance.pk:
            selected = self.instance.addresses.all()
            self.initial['addresses'] = [a.pk for a in selected]
        else:
            selected = []

        field.widget.choices = [(a.pk, str(a)) for a in selected]




