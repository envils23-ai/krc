from django.urls import path
from .views import ClientCreateView, ClientListView, ClientUpdateView, ClientDeleteView
from .views import ClientExcelExportView, ClientPdfExportView, ClientNewItemsView

urlpatterns = [
    path('new/', ClientCreateView.as_view(), name='client_new'),
    path('list/', ClientListView.as_view(), name='client_list'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path('<int:pk>/export/excel/', ClientExcelExportView.as_view(), name='client_export_excel'),
    path('<int:pk>/export/pdf/', ClientPdfExportView.as_view(), name='client_export_pdf'),
    path('list/new/', ClientNewItemsView.as_view(), name='client_list_new'),



]



