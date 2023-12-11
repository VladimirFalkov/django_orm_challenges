"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse, JsonResponse
from challenges.models import Post
from datetime import datetime, timedelta


def last_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    posts = Post.objects.filter(status="published").order_by("-created_at")[:3]
    print(posts)
    context = [post.to_json() for post in posts]
    return JsonResponse(context, safe=False)


def posts_search_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    parameter_query = request.GET.get("query")
    posts = Post.objects.filter(title__icontains=parameter_query)
    context = [post.to_json() for post in posts]
    return JsonResponse(context, safe=False)


def untagged_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Post.objects.filter(category__isnull=True).order_by(
        "author_full_name", "created_at"
    )
    context = [post.to_json() for post in posts]
    return JsonResponse(context, safe=False)


def categories_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories = request.GET.get("categories")
    print(request.GET)
    print(categories)
    if not categories:
        return HttpResponse(status=403)
    posts = Post.objects.filter(category__name__in=categories.split(","))
    context = [post.to_json() for post in posts]
    return JsonResponse(context, safe=False)


def last_days_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days = request.GET.get("last_days")
    if not last_days:
        return HttpResponse(status=403)
    date_for_query = datetime.now() - timedelta(days=int(last_days))
    posts = Post.objects.filter(published_at__gte=date_for_query)
    context = [post.to_json() for post in posts]
    return JsonResponse(context, safe=False)
