from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import BankService, BankRequest, BankServiceInRequest

# ----------------------------------------------------------------------
# 1. СТРАНИЦА СПИСКА УСЛУГ (ГЛАВНАЯ)
# ----------------------------------------------------------------------
def bankservice_list(request):
    query = request.GET.get('q', '')
    services = BankService.objects.filter(is_active=True)
    if query:
        services = services.filter(name__icontains=query)

    # Получаем текущую заявку-черновик для пользователя
    user = User.objects.first()
    current_request = BankRequest.objects.filter(client=user, status=BankRequest.Status.DRAFT).first()
    total_items = 0
    if current_request:
        total_items = BankServiceInRequest.objects.filter(request=current_request).count()

    context = {
        'bankservices': services,
        'bank_request': current_request,
        'total_items': total_items,
        'query': query,
    }
    return render(request, 'lab1/bankservice_list.html', context)

# ----------------------------------------------------------------------
# 2. ДЕТАЛЬНАЯ СТРАНИЦА УСЛУГИ
# ----------------------------------------------------------------------
def bankservice_detail(request, bankservice_id):
    service = get_object_or_404(BankService, id=bankservice_id, is_active=True)
    return render(request, 'lab1/bankservice_detail.html', {'bankservice': service})

# ----------------------------------------------------------------------
# 3. СТРАНИЦА ПРОСМОТРА ЗАЯВКИ
# ----------------------------------------------------------------------
def bank_request_detail(request, request_id):
    bank_request = get_object_or_404(BankRequest, id=request_id)
    if bank_request.status == BankRequest.Status.DELETED:
        return redirect('bankservice_list')

    # Получаем все связи "заявка-услуга"
    items_qs = BankServiceInRequest.objects.filter(request=bank_request).select_related('service')

    # Преобразуем в список словарей с нужными ключами
    items = []
    for item in items_qs:
        items.append({
            'bankservice_name': item.service.name,
            'bankservice_rate': item.service.rate,
            'bankservice_balance_account': item.service.balance_account,
            'bankservice_image': item.service.image,
            'bank_account': item.bank_account,
            'quantity': item.quantity,
        })

    context = {
        'bank_request': bank_request,
        'items': items,
    }
    return render(request, 'lab1/bank_request.html', context)

# ----------------------------------------------------------------------
# 4. ДОБАВЛЕНИЕ УСЛУГИ В ЗАЯВКУ (ЧЕРЕЗ ORM)
# ----------------------------------------------------------------------
@require_POST
def add_to_request(request, service_id):
    service = get_object_or_404(BankService, id=service_id, is_active=True)
    user = User.objects.first()
    # Найти или создать черновик заявки для этого пользователя
    bank_request, created = BankRequest.objects.get_or_create(
        client=user,
        status=BankRequest.Status.DRAFT,
        defaults={'status': BankRequest.Status.DRAFT}
    )
    # Добавить услугу (или увеличить количество, если уже есть)
    item, created = BankServiceInRequest.objects.get_or_create(
        request=bank_request,
        service=service,
        defaults={'quantity': 1, 'bank_account': '40802810600000005678'}
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect('bankservice_list')

# ----------------------------------------------------------------------
# 5. ЛОГИЧЕСКОЕ УДАЛЕНИЕ ЗАЯВКИ (ЧЕРЕЗ SQL UPDATE)
# ----------------------------------------------------------------------
def delete_request(request, request_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE bmstu_lab_bankrequest SET status = 'DELETED' WHERE id = %s",
                [request_id]
            )
        return redirect('bankservice_list')
    else:
        return redirect('bankservice_list')