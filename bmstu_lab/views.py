from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.views.decorators.http import require_POST
from .models import BankService, BankRequest, BankServiceInRequest, User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .minio_client import MinioClient
from .serializers import (
    BankServiceSerializer, BankServiceCreateSerializer,
    BankRequestSerializer, BankRequestUpdateSerializer,
    BankServiceInRequestSerializer, UserRegistrationSerializer
)

# ----------------------------------------------------------------------
# 1. СТРАНИЦА СПИСКА УСЛУГ (ГЛАВНАЯ)
# ----------------------------------------------------------------------
def bankservice_list(request):
    query = request.GET.get('q', '')
    services = BankService.objects.filter(is_deleted=False)
    if query:
        services = services.filter(name__icontains=query)

    current_request = BankRequest.objects.filter(status=BankRequest.Status.DRAFT).first()
    total_items = BankServiceInRequest.objects.filter(request=current_request).count() if current_request else 0

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
    service = get_object_or_404(BankService, id=bankservice_id, is_deleted=False)
    return render(request, 'lab1/bankservice_detail.html', {'bankservice': service})

# ----------------------------------------------------------------------
# 3. СТРАНИЦА ПРОСМОТРА ЗАЯВКИ
# ----------------------------------------------------------------------
def bank_request_detail(request, bank_request_id):
    bank_request = get_object_or_404(BankRequest, id=bank_request_id)
    if bank_request.status == BankRequest.Status.DELETED:
        return redirect('bank_services_list')

    items_qs = BankServiceInRequest.objects.filter(request=bank_request).select_related('service')
    items = []
    for item in items_qs:
        items.append({
            'bankservice_name': item.service.name,
            'bankservice_balance_account': item.service.balance_account,
            'bankservice_image': item.service.image,
            'bank_account': item.bank_account,
            'price': item.service_cost,
        })

    context = {
        'bank_request': bank_request,
        'items': items,
        'client_name': bank_request.client_name,
    }
    return render(request, 'lab1/bank_request.html', context)

# ----------------------------------------------------------------------
# 4. ДОБАВЛЕНИЕ УСЛУГИ В ЗАЯВКУ (ЧЕРЕЗ ORM) ДЛЯ ШАБЛОНОВ
# ----------------------------------------------------------------------
@require_POST
def add_to_request(request, bankservice_id):
    service = get_object_or_404(BankService, id=bankservice_id, is_deleted=False)

    bank_request, created = BankRequest.objects.get_or_create(
        status=BankRequest.Status.DRAFT,
        defaults={'status': BankRequest.Status.DRAFT}
    )
    BankServiceInRequest.objects.get_or_create(
        request=bank_request,
        service=service
    )
    return redirect('bank_services_list')

# ----------------------------------------------------------------------
# 5. ЛОГИЧЕСКОЕ УДАЛЕНИЕ ЗАЯВКИ (ЧЕРЕЗ SQL UPDATE) ДЛЯ ШАБЛОНОВ
# ----------------------------------------------------------------------
def delete_request(request, bank_request_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE bmstu_lab_bankrequest SET status = 'DELETED' WHERE id = %s",
                [bank_request_id]
            )
        return redirect('bank_services_list')
    else:
        return redirect('bank_services_list')

# ----------------------------------------------------------------------
# 6. ЛАБОРАТОРНАЯ 3 и 4 (API)
# ----------------------------------------------------------------------
def get_moderator():
    mod, _ = User.objects.get_or_create(username='moderator', defaults={'password': 'modpass', 'is_moderator': True})
    return mod

# ---------- Услуги ----------
@csrf_exempt
@api_view(['GET'])
def api_service_list(request):
    queryset = BankService.objects.filter(is_deleted=False)
    name = request.query_params.get('name')
    if name:
        queryset = queryset.filter(name__icontains=name)
    serializer = BankServiceSerializer(queryset, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def api_service_detail(request, pk):
    service = get_object_or_404(BankService, pk=pk, is_deleted=False)
    serializer = BankServiceSerializer(service)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def api_service_create(request):
    minio_client = MinioClient()
    image_file = request.FILES.get('image')
    video_file = request.FILES.get('video')
    image_key = minio_client.upload_file(image_file, 'img') if image_file else None
    video_key = minio_client.upload_file(video_file, 'video') if video_file else None

    serializer = BankServiceCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    service = serializer.save(image=image_key, video=video_key, is_deleted=False)
    return Response(BankServiceSerializer(service).data, status=status.HTTP_201_CREATED)

# ---------- Заявки ----------
@csrf_exempt
@api_view(['GET'])
def api_request_list(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)

    queryset = BankRequest.objects.exclude(status__in=[BankRequest.Status.DRAFT, BankRequest.Status.DELETED])
    if not request.user.is_moderator:
        queryset = queryset.filter(created_by=request.user)

    formed_from = request.query_params.get('formed_from')
    formed_to = request.query_params.get('formed_to')
    if formed_from:
        queryset = queryset.filter(formed_at__gte=formed_from)
    if formed_to:
        queryset = queryset.filter(formed_at__lte=formed_to)
    status_param = request.query_params.get('status')
    if status_param:
        queryset = queryset.filter(status=status_param)

    serializer = BankRequestSerializer(queryset, many=True)
    for data in serializer.data:
        req = BankRequest.objects.get(id=data['id'])
        cnt = BankServiceInRequest.objects.filter(request=req, bank_account__isnull=False).count()
        data['non_empty_items_count'] = cnt
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def api_request_detail(request, pk):
    bank_request = get_object_or_404(BankRequest, pk=pk)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    if bank_request.created_by != request.user and not request.user.is_moderator:
        return Response({'error': 'Access denied'}, status=403)
    if bank_request.status == BankRequest.Status.DELETED:
        return Response({'error': 'Заявка удалена'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BankRequestSerializer(bank_request)
    return Response(serializer.data)

@csrf_exempt
@api_view(['PUT'])
def api_request_update(request, pk):
    bank_request = get_object_or_404(BankRequest, pk=pk)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    if bank_request.created_by != request.user and not request.user.is_moderator:
        return Response({'error': 'Access denied'}, status=403)

    serializer = BankRequestUpdateSerializer(bank_request, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(BankRequestSerializer(bank_request).data)

@csrf_exempt
@api_view(['DELETE'])
def api_request_delete(request, pk):
    bank_request = get_object_or_404(BankRequest, pk=pk)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    if bank_request.created_by != request.user and not request.user.is_moderator:
        return Response({'error': 'Access denied'}, status=403)

    bank_request.status = BankRequest.Status.DELETED
    bank_request.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['PUT'])
def api_request_form(request, pk):
    bank_request = get_object_or_404(BankRequest, pk=pk)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    if bank_request.created_by != request.user:
        return Response({'error': 'You are not the owner of this request'}, status=403)
    if bank_request.status != BankRequest.Status.DRAFT:
        return Response({'error': 'Сформировать можно только черновик'}, status=400)
    if not bank_request.client_name.strip():
        return Response({'error': 'Не указано ФИО клиента'}, status=400)

    bank_request.status = BankRequest.Status.FORMED
    bank_request.formed_at = timezone.now()
    bank_request.save()
    return Response(BankRequestSerializer(bank_request).data)

@csrf_exempt
@api_view(['PUT'])
def api_request_complete(request, pk):
    if not request.user.is_authenticated or not request.user.is_moderator:
        return Response({'error': 'Only moderator can complete/reject request'}, status=403)

    bank_request = get_object_or_404(BankRequest, pk=pk)
    if bank_request.status != BankRequest.Status.FORMED:
        return Response({'error': 'Завершить/отклонить можно только сформированную заявку'}, status=400)
    action = request.data.get('action')
    if action not in ['complete', 'reject']:
        return Response({'error': 'action must be "complete" or "reject"'}, status=400)

    total = sum(item.service_cost for item in bank_request.bankserviceinrequest_set.all())
    bank_request.total_cost = str(total)

    if not bank_request.moderator:
        bank_request.moderator = request.user
    bank_request.completed_at = timezone.now()
    bank_request.status = BankRequest.Status.COMPLETED if action == 'complete' else BankRequest.Status.REJECTED
    bank_request.save()
    return Response(BankRequestSerializer(bank_request).data)

# ---------- М-М (услуги в заявке) ----------
@csrf_exempt
@api_view(['POST'])
def api_add_service_to_request(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)

    service_id = request.data.get('service_id')
    bank_account = request.data.get('bank_account')
    service_cost = request.data.get('service_cost')

    if not service_id:
        return Response({'error': 'service_id required'}, status=400)
    if service_cost is None:
        return Response({'error': 'service_cost required'}, status=400)

    service = get_object_or_404(BankService, id=service_id, is_deleted=False)

    draft, _ = BankRequest.objects.get_or_create(
        created_by=request.user,
        status=BankRequest.Status.DRAFT,
        defaults={'status': BankRequest.Status.DRAFT, 'created_by': request.user}
    )

    if BankServiceInRequest.objects.filter(request=draft, service=service).exists():
        return Response({'error': 'Service already in this request'}, status=400)

    item = BankServiceInRequest.objects.create(
        request=draft,
        service=service,
        bank_account=bank_account,
        service_cost=service_cost
    )
    return Response(BankServiceInRequestSerializer(item).data, status=201)

@csrf_exempt
@api_view(['DELETE'])
def api_remove_service_from_request(request):
    request_id = request.query_params.get('request_id')
    service_id = request.query_params.get('service_id')
    if not request_id or not service_id:
        return Response({'error': 'request_id and service_id required'}, status=400)

    bank_request = get_object_or_404(BankRequest, id=request_id)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    if bank_request.created_by != request.user and not request.user.is_moderator:
        return Response({'error': 'Access denied'}, status=403)

    service = get_object_or_404(BankService, id=service_id)
    item = get_object_or_404(BankServiceInRequest, request=bank_request, service=service)
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['PUT'])
def api_update_request_item(request):
    request_id = request.query_params.get('request_id')
    service_id = request.query_params.get('service_id')
    if not request_id or not service_id:
        return Response({'error': 'request_id and service_id required'}, status=400)

    bank_request = get_object_or_404(BankRequest, id=request_id)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    if bank_request.created_by != request.user and not request.user.is_moderator:
        return Response({'error': 'Access denied'}, status=403)

    service = get_object_or_404(BankService, id=service_id)
    item = get_object_or_404(BankServiceInRequest, request=bank_request, service=service)
    bank_account = request.data.get('bank_account')
    if bank_account is not None:
        item.bank_account = bank_account
        item.save()
    return Response(BankServiceInRequestSerializer(item).data)

# ---------- Иконка корзины ----------
@csrf_exempt
@api_view(['GET'])
def api_cart_icon(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    draft = BankRequest.objects.filter(created_by=request.user, status=BankRequest.Status.DRAFT).first()
    if draft:
        items_count = BankServiceInRequest.objects.filter(request=draft).count()
        return Response({'bank_request_id': draft.id, 'items_count': items_count})
    return Response({'bank_request_id': None, 'items_count': 0})

# ---------- Пользователи ----------
@csrf_exempt
@api_view(['POST'])
def api_register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

@extend_schema(
    request=inline_serializer(
        name='LoginRequest',
        fields={
            'username': serializers.CharField(),
            'password': serializers.CharField(),
        }
    ),
    responses={200: inline_serializer(
        name='LoginResponse',
        fields={
            'status': serializers.CharField(),
            'username': serializers.CharField(),
            'is_moderator': serializers.BooleanField(),
        }
    )}
)
@csrf_exempt
@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'username and password required'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'status': 'ok',
            'username': user.username,
            'is_moderator': user.is_moderator
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({'status': 'ok'})