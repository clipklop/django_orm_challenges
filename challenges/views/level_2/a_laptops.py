"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
import json
from decimal import Decimal

from django.http import HttpRequest, JsonResponse

from challenges.models import Notebook

from challenges.utils.serializer import to_json


def laptop_details_view(request: HttpRequest, laptop_id: int) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    laptop = Notebook.objects.filter(id=laptop_id)

    if not laptop:
        return JsonResponse(status=404, data={'message': f"The ID {laptop_id} hasn't been found."})
    # Преобразую в dict, чтобы JsonResponse красивее отображал пейлоад без экранированных символов
    laptop_serialize = json.loads(to_json(laptop))

    return JsonResponse(laptop_serialize, safe=False)
    


def laptop_in_stock_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Notebook.objects.filter(qty__gte=1)
    laptop_serialize = json.loads(to_json(laptops))

    return JsonResponse(laptop_serialize, safe=False)


def laptop_filter_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    get_brand = request.GET.get('brand')
    get_price = request.GET.get('min_price')
    if not get_brand or not get_price:
        return JsonResponse(status=404, data={'message': f"Missing 'brand' and 'min_price' parameters in the query"})

    check_brand = Notebook.objects.filter(brand=get_brand)
    if not check_brand:
        return JsonResponse(status=403, data={'message': f"No such brand - '{get_brand}' in our DB."})
    
    try:
        coerce_price = Decimal(get_price)
    except:
        coerce_price = Decimal(0)
    if coerce_price < 0:
        return JsonResponse(status=403, data={'message': "Only positive value of 'min_price' is allowed."})

    filter_laptops = Notebook.objects.filter(price__gte=coerce_price).order_by('price')
    laptops_serialize = json.loads(to_json(filter_laptops, fields=('price', 'brand')))

    return JsonResponse(laptops_serialize, safe=False)


def last_laptop_details_view(request: HttpRequest) -> JsonResponse: # кажется, опечатка. laptop_id здесь не нужен
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    laptops = Notebook.objects.order_by('id').reverse()[:1]
    if not laptops:
        return JsonResponse(status=404, data={'message': f"Currently there are no laptops available in our DB."})

    laptops_serialize = json.loads(to_json(laptops))

    return JsonResponse(laptops_serialize, safe=False)
