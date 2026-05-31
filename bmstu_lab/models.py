from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Модель услуги (банковский продукт)
class BankService(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    balance_account = models.CharField(max_length=5, verbose_name="Балансовый счёт")
    description = models.TextField(verbose_name="Описание")
    image = models.CharField(max_length=100, blank=True, null=True, verbose_name="Изображение")
    video = models.CharField(max_length=100, blank=True, null=True, verbose_name="Видео")
    is_deleted = models.BooleanField(default=False, verbose_name="Мягкое удаление")
    #price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость услуги")

    def __str__(self):
        return self.name

# Модель заявки
class BankRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        DELETED = 'DELETED', 'Удалён'
        FORMED = 'FORMED', 'Сформирован'
        COMPLETED = 'COMPLETED', 'Завершён'
        REJECTED = 'REJECTED', 'Отклонён'

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    formed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_cost = models.CharField(max_length=50, blank=True, null=True)

    # Клиент – строка (ФИО бабушки)
    client_name = models.CharField(max_length=150, blank=True, verbose_name="ФИО клиента")

    # Операционист (сотрудник, создавший заявку) – пока NULL, в ЛР4 заполним
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='created_requests',
        verbose_name="Операционист"
    )

    # Модератор (завершивший заявку) – заполняется при завершении
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='moderated_requests',
        verbose_name="Модератор"
    )

    def __str__(self):
        return f"Заявка №{self.id}"

# Модель связи "услуги в заявке" (многие-ко-многим с доп. полями)
class BankServiceInRequest(models.Model):
    request = models.ForeignKey(BankRequest, on_delete=models.DO_NOTHING, verbose_name="Заявка")
    service = models.ForeignKey(BankService, on_delete=models.DO_NOTHING, verbose_name="Услуга")
    bank_account = models.CharField(max_length=20, blank=True, null=True, verbose_name="Банковский счёт клиента")
    service_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Комиссия за услугу")

    class Meta:
        unique_together = ('request', 'service')   # составной уникальный ключ

    def __str__(self):
        return f"{self.request} – {self.service}"

# Модель пользователя (проверка роли модератора у пользователя)
class User(AbstractUser):
    is_moderator = models.BooleanField(default=False, verbose_name="Модератор")

    class Meta:
        db_table = 'auth_user'