
### 📝 README для лабораторной №3 (ветка `lab3-api`)

Аналогично, создайте `README.md` в ветке `lab3-api`:

```markdown
# Лабораторная работа №3: Веб-сервис (API) для банковских услуг

## Цель работы
Создание REST API с полной бизнес-логикой (16 эндпоинтов), интеграция с MinIO для загрузки файлов, фильтрация заявок, расчёт стоимости услуг, регистрация пользователей.

## Технологии
- Django, Django REST Framework
- PostgreSQL, MinIO
- Insomnia/Postman для тестирования

## API эндпоинты (домены)

### Услуги
- `GET /api/bank_services/?name=...` – список с фильтром
- `GET /api/bank_services/{id}/` – одна услуга
- `POST /api/bank_services/create/` – создание услуги с загрузкой изображения и видео (имена файлов генерируются на латинице)

### Заявки
- `GET /api/bank_requests/` – список (исключая черновики и удалённые) с фильтрацией по `formed_from`, `formed_to`, `status`
- `GET /api/bank_requests/{id}/` – детали заявки с услугами
- `PUT /api/bank_requests/{id}/update/` – изменение полей заявки (заглушка)
- `PUT /api/bank_requests/{id}/form/` – формирование заявки (расчёт `total_cost`)
- `PUT /api/bank_requests/{id}/complete/` – завершение/отклонение модератором
- `DELETE /api/bank_requests/{id}/delete/` – логическое удаление
- `GET /api/bank_cart/` – иконка корзины (id черновика, количество)

### Связь услуги-заявки
- `POST /api/bank_request_items/add/` – добавить услугу в черновик
- `DELETE /api/bank_request_items/remove/` – удалить услугу из заявки
- `PUT /api/bank_request_items/update/` – изменить `bank_account`

### Пользователи
- `POST /api/bank_users/register/` – регистрация
- `POST /api/bank_users/login/` – заглушка
- `POST /api/bank_users/logout/` – заглушка

## Тестирование (коллекция Insomnia)
Коллекция из 16 запросов прилагается (файл `Insomnia_collection.json`). Скриншоты выполнения – в папке `screenshots/lab3/`.

## Демонстрация фильтрации
Пример фильтрации заявок по дате и статусу: