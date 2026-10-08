from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    model = Client

admin.site.register(Client)