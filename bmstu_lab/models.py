from django.db import models
from django.contrib.auth.models import User

# Модель услуги (банковский продукт)
class BankService(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    rate = models.CharField(max_length=20, verbose_name="Ставка/процент")
    amount = models.CharField(max_length=50, verbose_name="Сумма/лимит")
    term = models.CharField(max_length=50, verbose_name="Срок")
    balance_account = models.CharField(max_length=5, verbose_name="Балансовый счёт")
    description = models.TextField(verbose_name="Описание")
    image = models.CharField(max_length=100, blank=True, null=True, verbose_name="Изображение (ключ в Minio)")
    video = models.CharField(max_length=100, blank=True, null=True, verbose_name="Видео (ключ в Minio)")
    is_deleted = models.BooleanField(default=False, verbose_name="Флаг мягкого удаления")

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

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    formed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата формирования")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    client_name = models.CharField(max_length=150, verbose_name="ФИО клиента", default="Клиент по умолчанию")
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='managed_requests', verbose_name="Менеджер")
    total_cost = models.CharField(max_length=50, blank=True, null=True, verbose_name="Стоимость обслуживания")

    def __str__(self):
        return f"Заявка №{self.id}"

# Модель связи "услуги в заявке" (многие-ко-многим с доп. полями)
class BankServiceInRequest(models.Model):
    request = models.ForeignKey(BankRequest, on_delete=models.DO_NOTHING, verbose_name="Заявка")
    service = models.ForeignKey(BankService, on_delete=models.DO_NOTHING, verbose_name="Услуга")
    bank_account = models.CharField(max_length=20, blank=True, null=True, verbose_name="Банковский счёт клиента")

    class Meta:
        unique_together = ('request', 'service')   # составной уникальный ключ

    def __str__(self):
        return f"{self.request} – {self.service}"