from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator



class Client(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_code = models.BigIntegerField( null=True, blank=True, verbose_name='Код клієнта')
    client_name = models.CharField(max_length=100,null=False, blank=False, verbose_name='Назва клієнта')
    client_registration_region = models.CharField(max_length=100, blank=True, null=True, verbose_name='Регіон реєстрації')
    client_registration_city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Місто реєстрації')
    email = models.EmailField(blank=True, null=True, verbose_name='Электронна пошта')
    # client_phone_number = models.BigIntegerField(blank=True, null=True, verbose_name='Номер телефону')
    client_phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[RegexValidator(r"^\d{10}$", "Введіть 10 цифр, наприклад 0960663212")],
        verbose_name='Номер телефону',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def phone_display(self):
        p = self.client_phone_number or ""
        if len(p) == 10 and p.isdigit():
            return f"({p[:3]}) {p[3:6]} {p[6:8]} {p[8:]}"
        return p

    def __str__(self):
        return self.client_name

    def get_absolute_url(self):
        return reverse ('client_detail', kwargs={'pk': self.pk})
