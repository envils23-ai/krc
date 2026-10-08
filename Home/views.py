from Client.models import Client
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from adress.models import ClientAddress

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Считает общее количество записей в базе
        context["total_clients"] = Client.objects.count()
        context["total_clients_address"] = ClientAddress.objects.count()
        return context
