from django.shortcuts import render, redirect

bankservices = [
    {
        'id': 1,
        'name': 'Кредит для бизнеса',
        'rate': 'от 16%',
        'balance_account': '40701',
        "description": 'Кредит на покупку оборудования, пополнение оборотных средств или модернизацию производства',
        'image': 'credity_KB.png',
        'video': 'credit.mp4',

    },
    {
        'id': 2,
        'name': 'Расчетный счет для бизнеса',
        'rate': '0 ₽ обслуживание',
        'balance_account': '40702',
        "description": 'Открытие онлайн, бесплатные переводы внутри банка, персональный менеджер',
        'image': 'diploma.jpg',
        'video': 'Video cash.mp4',
    },
    {
        'id': 3,
        'name': 'Кредитная карта',
        'rate': 'от 3%',
        'balance_account': '40801',
        "description": 'Кэшбэк до 5%, бесплатное обслуживание при тратах от 5 000 ₽/мес.',
        'image': 'credit_card.jpg',
        'video': 'credit_card.mp4',
    },
    {
        'id': 4,
        'name': 'Депозит',
        'rate': 'до 14%',
        'balance_account': '40703',
        "description": 'Гибкие условия, пополнение и частичное снятие',
        'image': 'deposit.webp',
        'video': 'deposit.mp4',
    },
    {
        'id': 5,
        'name': 'Эквайринг',
        'rate': 'от 1,5%',
        'balance_account': '40704',
        "description": 'Приём карт, оплата по QR-коду, онлайн-касса в подарок',
        'image': 'acquiring.jpg',
        'video': 'acquaring.mp4',
    }
]

bank_request = {
    'id': 101,
    'client_name': 'Иванов Иван Иванович',
    'total_cost': '1 500 ₽',
    'items': [
        {
            'bankservice_id': 1,
            'quantity': 2,
            'bank_account': '40802810600000005678',
        },
{
            'bankservice_id': 2,
            'quantity': 1,
            'bank_account': '40802810700000004444',
        },
        {
            'bankservice_id': 3,
            'quantity': 1,
            'bank_account': '40802810700000009123',
        },
        {
            'bankservice_id': 4,
            'quantity': 4,
            'bank_account': '40802810700000005489',
        },
        {
            'bankservice_id': 5,
            'quantity': 6,
            'bank_account': '40802810700000003256',
        },
    ],
}

# Контроллер для страницы списка услуг (главная)
def bankservice_list(request):
    query = request.GET.get('q', '')
    if query:
        filtered_bankservices = [s for s in bankservices if query.lower() in s['name'].lower()]
        if not filtered_bankservices:
            filtered_bankservices = bankservices
    else:
        filtered_bankservices = bankservices

    # считаем общее количество позиций в заявке
    total_items = sum(item['quantity'] for item in bank_request['items'])

    context = {
        'bankservices': filtered_bankservices,
        'bank_request': bank_request,
        'total_items': total_items,
        'query': query,
    }
    return render(request, 'lab1/bankservice_list.html', context)

# Контроллер для детальной страницы услуги
def bankservice_detail(request, bankservice_id):
    bankservice = next((s for s in bankservices if s['id'] == bankservice_id), None)
    if not bankservice:
        return redirect('bankservice_list')  # если нет такой услуги
    return render(request, 'lab1/bankservice_detail.html', {'bankservice': bankservice})

# Контроллер для страницы заявки
def bank_request_detail(request, request_id):
    if request_id != bank_request['id']:
        return redirect('bankservice_list')
    # обогащаем элементы заявки данными об услугах

    items = []  # <-- добавьте эту строку

    for item in bank_request['items']:
        bankservice = next((s for s in bankservices if s['id'] == item['bankservice_id']), None)
        if bankservice:
            items.append({
                'bankservice_name': bankservice['name'],
                'bankservice_rate': bankservice['rate'],
                'bankservice_balance_account': bankservice['balance_account'],
                'bankservice_image': bankservice['image'],
                'quantity': item['quantity'],
                'bank_account': item['bank_account'],
            })
    context = {
        'bank_request': bank_request,
        'items': items,
    }
    return render(request, 'lab1/bank_request.html', context)