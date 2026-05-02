"""
URL configuration for bmstu_lab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from bmstu_lab import views

urlpatterns = [
    path('', views.bankservice_list, name='bank_services_list'),
    path('bankservice/<int:bankservice_id>/', views.bankservice_detail, name='bank_services_detail'),
    path('bankrequest/<int:bank_request_id>/', views.bank_request_detail, name='bank_request_detail'),
    path('add-to-request/<int:bankservice_id>/', views.add_to_request, name='bank_add_to_request'),
    path('delete-request/<int:bank_request_id>/', views.delete_request, name='bank_delete_request'),
    path('api/bank_services/', views.api_service_list, name='api_service_list'),
    path('api/bank_services/<int:pk>/', views.api_service_detail, name='api_service_detail'),
    path('api/bank_services/create/', views.api_service_create, name='api_service_create'),
    path('api/bank_requests/', views.api_request_list, name='api_request_list'),
    path('api/bank_requests/<int:pk>/', views.api_request_detail, name='api_request_detail'),
    path('api/bank_requests/<int:pk>/update/', views.api_request_update, name='api_request_update'),
    path('api/bank_requests/<int:pk>/delete/', views.api_request_delete, name='api_request_delete'),
    path('api/bank_requests/<int:pk>/form/', views.api_request_form, name='api_request_form'),
    path('api/bank_requests/<int:pk>/complete/', views.api_request_complete, name='api_request_complete'),
    path('api/bank_request_items/add/', views.api_add_service_to_request, name='api_add_service_to_request'),
    path('api/bank_request_items/remove/', views.api_remove_service_from_request, name='api_remove_service_from_request'),
    path('api/bank_request_items/update/', views.api_update_request_item, name='api_update_request_item'),
    path('api/bank_cart/', views.api_cart_icon, name='api_cart_icon'),
    path('api/bank_users/register/', views.api_register, name='api_register'),
    path('api/bank_users/login/', views.api_login_stub, name='api_login'),
    path('api/bank_users/logout/', views.api_logout_stub, name='api_logout'),
]
