from django.contrib import admin
from .models import ClientAddress

class ClientAddressAdmin(admin.ModelAdmin):
    model = ClientAddress


admin.site.register(ClientAddress
)