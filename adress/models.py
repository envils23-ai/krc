from datetime import timezone

from django.db import models
from django.conf import settings
from django.urls import reverse
from Client.models import Client
from django.utils import timezone
import re


# def _natural_key(value):
#     # "12А" -> ['', 12, 'а']: регистр игнорируется, числа сравниваются как числа
#     return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', value or '')]

class ClientAddress(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ForeignKey( Client,on_delete=models.CASCADE,related_name='addresses',verbose_name='Клієнт', blank=True, null=True)
    client_adress_region = models.CharField(max_length=100, blank=True, null=True, verbose_name='Область')
    client_adress_city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Місто')
    client_adress_street = models.CharField(max_length=100, blank=False, null=True, verbose_name='Вулиця')
    client_adress_building_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Номер будівлі')
    client_adress_phone_number = models.BigIntegerField(blank=True, null=True, verbose_name='Номер телефону дільниці')
    created_at = models.DateTimeField(auto_now_add=True)

    # @property
    # def full_address(self):
    #     parts = [
    #         self.client_adress_region,
    #         self.client_adress_city,
    #         self.client_adress_street,
    #         self.client_adress_building_number,
    #     ]
    #     return ', '.join(part for part in parts if part)

    def __str__(self):
        parts = [
            self.client_adress_region,
            self.client_adress_city,
            self.client_adress_street,
            self.client_adress_building_number,

        ]
        return ', '.join(p for p in parts if p) or f'Адреса #{self.pk}'


