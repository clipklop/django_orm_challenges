"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими постами для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект поста в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
import json
import datetime

from django.http import HttpRequest, JsonResponse

from challenges.models import BlogPost
from challenges.utils.serializer import to_json


def last_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    posts = BlogPost.objects.order_by('-id')[:3]

    post_serialize = json.loads(to_json(posts))

    return JsonResponse(post_serialize, safe=False)


def posts_search_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    get_query = request.GET.get('query')
    if not get_query:
        return JsonResponse(status=404, data={'message': f"Missing 'query' parameter in the query"})
    
    post_query = BlogPost.objects.filter(name__icontains=get_query, text__icontains=get_query)
    post_serialize = json.loads(to_json(post_query))

    return JsonResponse(post_serialize, safe=False)


def untagged_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = BlogPost.objects.filter(
        category__isnull=True
        ).order_by('author_name', 'creation_date')

    post_serialize = json.loads(to_json(posts))

    return JsonResponse(post_serialize, safe=False)


def categories_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    get_categories = request.GET.get('categories')
    if not get_categories:
        return JsonResponse(status=404, data={'message': f"Missing 'categories' parameter in the query"})
    
    list_categroies = get_categories.split(',')
    post_categories = BlogPost.objects.filter(category__in=list_categroies)
    post_serialize = json.loads(to_json(post_categories))

    return JsonResponse(post_serialize, safe=False)


def last_days_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    get_last_days = request.GET.get('last_days')
    if not get_last_days:
        return JsonResponse(status=404, data={'message': f"Missing 'last_days' parameter in the query"})
    print(datetime.date(get_last_days))
    post_last_days = BlogPost.objects.filter(creation_date__gte=datetime.date(get_last_days))
    post_serialize = json.loads(to_json(post_last_days))

    return JsonResponse(post_serialize, safe=False)
