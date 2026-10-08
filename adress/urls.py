from django.urls import path
from .views import ClientAddressCreateView, ClientAddressListView, ClientAddressUpdateView, ClientAddressDeleteView
from .views import AddressExcelExportView, AddressPdfExportView, FreeAddressSearchView


urlpatterns = [
    path('create/', ClientAddressCreateView.as_view(), name='client_address_new'),
    path('list/', ClientAddressListView.as_view(), name='client_address_list'),
    path('edit/<int:pk>/', ClientAddressUpdateView.as_view(), name='client_address_edit'),
    path("delete/<int:pk>/", ClientAddressDeleteView.as_view(), name="client_address_delete"),
    path('address/<int:pk>/export/excel/', AddressExcelExportView.as_view(), name='client_address_export_excel'),
    path('address/<int:pk>/export/pdf/', AddressPdfExportView.as_view(), name='client_address_export_pdf'),
    path('address/free-search/', FreeAddressSearchView.as_view(), name='free_address_search'),

]