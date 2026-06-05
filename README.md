markdown
# Лабораторная работа №5: Разработка базового одностраничного приложения на React

## Цель работы
Разработка одностраничного приложения (SPA) на React с использованием TypeScript, хуков, маршрутизации, фильтрации данных и mock-объектов. Приложение имитирует интерфейс банка услуг с тремя страницами, навигацией, хлебными крошками и корзиной (заявкой).

## Задание
Разработать три страницы фронтенд-приложения на ReactTS:
1. **Список услуг** – карточки услуг с изображениями (или заглушкой), фильтрацией по названию и дате, иконкой корзины.
2. **Детали услуги** – отображение видео (с автоповтором) и подробного описания.
3. **Корзина (заявка)** – таблица добавленных услуг с возможностью удаления заявки.

**Требования:**
- Использовать компоненты React-Bootstrap.
- Данные брать из mock-объектов (без бэкенда).
- Реализовать самописные Breadcrumbs, панель навигации (Navbar).
- Изображение по умолчанию при отсутствии картинки.
- Запрещены Redux и Context (только локальный state и поднятие состояния).
- На странице списка – иконка корзины счётчиком.
- Фильтры: поиск по названию, диапазон дат.

## Структура проекта (ключевые файлы)
frontend/
├── public/
│ └── placeholder.png
├── src/
│ ├── components/
│ │ ├── Breadcrumbs.tsx
│ │ ├── Navbar.tsx
│ │ └── ServiceCard.tsx
│ ├── data/
│ │ └── mockServices.ts
│ ├── pages/
│ │ ├── ServicesList.tsx
│ │ ├── ServiceDetail.tsx
│ │ └── BankCart.tsx
│ ├── App.tsx
│ ├── main.tsx
│ └── style.css
├── package.json
├── vite.config.ts
└── tsconfig.json


## Реализация трёх страниц

### 1. Страница списка услуг (`ServicesList.tsx`)
- **Состояния**: `searchName`, `startDate`, `endDate`, `cartItems` (Set).
- **Фильтрация** через `useMemo` (мемоизация отфильтрованного массива).  
  Фильтр по названию (регистронезависимый) и по дате (нормализация через `Date.UTC` для корректного сравнения без учёта времени).
- **Отображение**: сетка карточек (`services-grid`). Каждая карточка – компонент `ServiceCard`.
- **Корзина**: иконка `FaShoppingCart` + счётчик; при пустой корзине иконка серая и неактивная. Кнопка «Очистить заявку».
- **Переход на детали** – клик по карточке (весь блок, кроме кнопки «Добавить в заявку»).
### 2. Страница деталей услуги (`ServiceDetail.tsx`)
- Получает `id` из URL с помощью `useParams`.
- Находит услугу в `mockServices`.
- Отображает **видео** из MinIO (или статической папки) с атрибутами `autoPlay`, `loop`, `muted`, `playsInline` (без элементов управления).  
  При ошибке загрузки видео показывается изображение по умолчанию.
- Хлебные крошки: «Главная / Услуги / Название услуги».
### 3. Страница корзины (`BankCart.tsx`)
- Получает `cartItems` (Set ID) и `clearCart` через пропсы.
- Формирует таблицу с колонками: фото, услуга, балансовый счёт, банковский счёт (заглушка), стоимость.
- При пустой корзине – информационное сообщение.
- Кнопка «Удалить заявку» очищает корзину.
## Реализация изображения по умолчанию
- В компонентах `ServiceCard` и `ServiceDetail` определена константа:
  ```ts
  const DEFAULT_IMAGE = '/placeholder.png';

## URL изображения формируется как MINIO_BASE_URL + service.image или DEFAULT_IMAGE, если image === null.
Добавлен обработчик onError, который заменяет битую ссылку на DEFAULT_IMAGE:
<img src={imageUrl} onError={(e) => (e.currentTarget.src = DEFAULT_IMAGE)} />

## Состояния для фильтров:
const [searchName, setSearchName] = useState('');
const [startDate, setStartDate] = useState('');
const [endDate, setEndDate] = useState('');

## Хук useMemo для фильтрации:
const filteredServices = useMemo(() => {
  return mockServices.filter(service => {
    const nameMatch = service.name.toLowerCase().includes(searchName.toLowerCase());
    const normalize = (date: string) => Date.UTC(...date.split('T')[0].split('-'));
    let dateMatch = true;
    if (startDate && endDate) {
      dateMatch = normalize(service.created_at) >= normalize(startDate) &&
                  normalize(service.created_at) <= normalize(endDate);
    } else if (startDate) {
      dateMatch = normalize(service.created_at) >= normalize(startDate);
    } else if (endDate) {
      dateMatch = normalize(service.created_at) <= normalize(endDate);
    }
    return nameMatch && dateMatch;
  });
}, [searchName, startDate, endDate]);

## Почему useMemo?
– Фильтрация выполняется только при изменении зависимостей (поля поиска, даты). Это предотвращает лишние пересчёты при каждом рендере (например, при добавлении в корзину).
## Передача свойств (props)
ServicesList получает cartItems и setCartItems из App (поднятие состояния).
В ServiceCard передаются service (объект услуги) и onAddToCart (колбэк для добавления в корзину).
BankCart получает cartItems и clearCart.

## Используемые хуки
Хук	                      Где используется	                        Назначение
useState	                ServicesList, ServiceDetail, App	       Управление состоянием фильтров, корзины, ошибки видео.
useMemo	                  ServicesList	                           Мемоизация отфильтрованного списка услуг.
useNavigate	              ServiceCard	                             Программный переход на страницу деталей по клику на карточку.
useParams	                ServiceDetail	                           Получение id услуги из URL.
useEffect	                (не используется в данной работе)	       Для работы с реальным API понадобился бы для загрузки данных, но у нас mock.

## Дополнительные техники
Остановка всплытия события (e.stopPropagation()) в кнопке «Добавить в заявку», чтобы клик не вызывал переход на детали.
Set для корзины – гарантирует уникальность добавленных услуг.
Нормализация дат через Date.UTC – корректное сравнение без влияния часовых поясов.

## Панель навигации и Breadcrumbs
Navbar – компонент react-bootstrap/Navbar с синим фоном (цвет ВТБ) и брендом.
Breadcrumbs – самописный компонент, отображающий путь с иконкой дома и разделителями /. Активная страница выделяется полужирным шрифтом.