from django.views.generic.edit import CreateView
from .models import ClientAddress
from django.urls import reverse_lazy
from .forms import ClientAddressCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView
#Для DeleteView
from django.db.models import ProtectedError
from django.shortcuts import redirect
#Для Excel, PDF
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


from django.db.models import Q
from django.http import JsonResponse
from django.utils.html import format_html



class ClientAddressCreateView(LoginRequiredMixin,CreateView):
  model = ClientAddress
  template_name = 'client_address_new.html'
  form_class = ClientAddressCreationForm
  success_url = reverse_lazy('home')

  def form_valid(self, form):
    # Привязываем текущего пользователя к полю author перед сохранением
    form.instance.author = self.request.user
    # Сообщение о успешном создании клиента
    response = super().form_valid(form)
    messages.success(self.request, f"Адрес клієнта <strong>{self.object.full_address}</strong> вдало створений!")
    return super().form_valid(form)

class ClientAddressCreateView(LoginRequiredMixin, CreateView):
  model = ClientAddress
  template_name = 'client_address_new.html'
  form_class = ClientAddressCreationForm
  success_url = reverse_lazy('home')

  def form_valid(self, form):
    form.instance.author = self.request.user
    response = super().form_valid(form)

    address = ', '.join(filter(None, (
      self.object.client_adress_region,
      self.object.client_adress_city,
      self.object.client_adress_street,
      self.object.client_adress_building_number,
    )))
    messages.success(
      self.request,
      format_html('Адреса клієнта <strong>{}</strong> вдало створена!', address),
    )
    return response

class ClientAddressListView(LoginRequiredMixin, ListView):
  model = ClientAddress
  template_name = 'client_address_list.html'
  context_object_name = "ClientAddress"
  paginate_by = 10
  ordering = ["-created_at"]


#Поиск в фильтре
  def get_queryset(self):
    queryset = super().get_queryset()
    street = self.request.GET.get("street", "").strip()
    region = self.request.GET.get("region", "").strip()

    if street:
      queryset = queryset.filter(client_adress_street__icontains=street)
    if region:
      queryset = queryset.filter(client_adress_city__icontains=region)
    return queryset


# Сохраняем значения поиска при переходах по страницам пагинации
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["street"] = self.request.GET.get("street", "").strip()
    context["region"] = self.request.GET.get("region", "").strip()
    return context

class ClientAddressUpdateView(LoginRequiredMixin, UpdateView):
  model = ClientAddress
  template_name = 'client_address_edit.html'
  form_class = ClientAddressCreationForm
  success_url = reverse_lazy('client_address_list')

  def form_valid(self, form):
    # Привязываем текущего пользователя к полю author перед сохранением
    form.instance.author = self.request.user
    # Сообщение о успешном создании клиента
    response = super().form_valid(form)
    messages.success(self.request, f"Запис <strong>{self.object.client_adress_street}</strong> було змінено!")
    return response

class ClientAddressDeleteView(LoginRequiredMixin, DeleteView):
    model = ClientAddress
    success_url = reverse_lazy("client_address_list")
    context_object_name = "client_delete_address"

    # Теперь это не страница, а фрагмент, который htmx вставит в модальное окно
    template_name = "client_address_delete_modal.html"

    def get(self, request, *args, **kwargs):
      # htmx добавляет к каждому запросу заголовок HX-Request.
      # Если кто-то откроет адрес в браузере напрямую, не показываем
      # голый фрагмент, а возвращаем на список
      if not request.headers.get("HX-Request"):
        return redirect("client_address_list")
      return super().get(request, *args, **kwargs)

    def form_valid(self, form):
      # Без изменений: удаление и сообщение (POST)
      name = self.object.client_adress_street
      try:
        response = super().form_valid(form)
      except ProtectedError:
        messages.error(
          self.request,
          f"Неможливо видалити <strong>«{name}»</strong>: у клієнта є пов'язані адреси.",
        )
        return redirect("client_address_list")
      messages.success(self.request, f"Клієнта <strong>«{name}»</strong> видалено.")
      return response
    
ADDRESS_EXPORT_FIELDS = [
    'client_adress_region',
    'client_adress_city',
    'client_adress_street',
    'client_adress_building_number',
]

class AddressSingleExportMixin(LoginRequiredMixin):
  def get_address(self):
    return get_object_or_404(
      ClientAddress.objects.select_related('client'),
      pk=self.kwargs['pk'],
    )

  @staticmethod
  def get_rows(address):
    rows = []
    for f in ADDRESS_EXPORT_FIELDS:
      label = str(ClientAddress._meta.get_field(f).verbose_name)
      value = getattr(address, f)
      rows.append((label, '' if value is None else str(value)))

    client_name = address.client.client_name if address.client else ''
    rows.append(('Клієнт', client_name))
    return rows


class AddressExcelExportView(AddressSingleExportMixin, View):
  def get(self, request, *args, **kwargs):
    address = self.get_address()

    wb = Workbook()
    ws = wb.active
    ws.title = 'Адреса'

    ws.append(['Поле', 'Значення'])
    for cell in ws[1]:
      cell.font = Font(bold=True)

    for label, value in self.get_rows(address):
      ws.append([label, value])

    for idx, column in enumerate(ws.columns, start=1):
      max_len = max(len(str(c.value or '')) for c in column)
      ws.column_dimensions[get_column_letter(idx)].width = min(max_len + 2, 60)

    response = HttpResponse(
      content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="address_{address.pk}.xlsx"'
    wb.save(response)
    return response


class AddressPdfExportView(AddressSingleExportMixin, View):
  FONT_NAME = 'DejaVuSans'

  def register_font(self):
    if self.FONT_NAME in pdfmetrics.getRegisteredFontNames():
      return
    candidates = [
      settings.BASE_DIR / 'fonts' / 'DejaVuSans.ttf',
      Path(r'C:\Windows\Fonts\arial.ttf'),
      Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
    ]
    font_path = next((p for p in candidates if p.exists()), None)
    if font_path is None:
      raise FileNotFoundError('Не найден шрифт с кириллицей для PDF')
    pdfmetrics.registerFont(TTFont(self.FONT_NAME, str(font_path)))

  def get(self, request, *args, **kwargs):
    address = self.get_address()
    self.register_font()

    style = ParagraphStyle('cell', fontName=self.FONT_NAME, fontSize=10, leading=13)
    head_style = ParagraphStyle('head', parent=style, textColor=colors.white)

    data = [[Paragraph('Поле', head_style), Paragraph('Значення', head_style)]]
    for label, value in self.get_rows(address):
      data.append([Paragraph(label, style), Paragraph(value, style)])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="address_{address.pk}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    table = Table(data, colWidths=[170, None], repeatRows=1)
    table.setStyle(TableStyle([
      ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
      ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
      ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
    ]))
    doc.build([table])
    return response

#Поиск адессов для добавления поля
class FreeAddressSearchView(LoginRequiredMixin, View):
  limit = 30

  def get(self, request):
    q = request.GET.get('q', '').strip()
    client_pk = request.GET.get('client', '')

    available = Q(client__isnull=True)
    if client_pk.isdigit():
      available |= Q(client_id=int(client_pk))

    qs = ClientAddress.objects.filter(available)
    if q:
      qs = qs.filter(
        Q(client_adress_street__icontains=q) |
        Q(client_adress_city__icontains=q) |
        Q(client_adress_region__icontains=q)
      )
    qs = qs.order_by('client_adress_street')[:self.limit]
    return JsonResponse({'results': [{'id': a.pk, 'text': str(a)} for a in qs]})