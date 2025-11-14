from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category

POSTS_PER_PAGE_ON_INDEX = 5


def _get_base_posts_queryset():
    """Возвращает список объектов для постов с базовыми фильтрами и select_related"""
    now = timezone.now()
    base_filters = {
        'pub_date__lte': now,
        'is_published': True,
        'category__is_published': True,
    }

    select_related_fields = ['author', 'category', 'location']

    queryset = Post.objects.filter(**base_filters) \
        .select_related(*select_related_fields)
    return queryset


def index(request):
    """Отображает главную страницу блога со списком последних публикаций"""
    posts_list = _get_base_posts_queryset()

    posts_list = posts_list[:POSTS_PER_PAGE_ON_INDEX] 

    context = {"posts": posts_list}
    return render(request, "blog/index.html", context)


def post_detail(request, post_id):
    """Отображает детальную страницу поста по его ID"""
    post_queryset = _get_base_posts_queryset()

    post = get_object_or_404(post_queryset, pk=post_id)

    context = {"post": post}
    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):
    """Отображает страницу категории"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts_list = _get_base_posts_queryset()

    posts_list = posts_list.filter(category=category)

    context = {
        'posts': posts_list,
        'category': category,
    }
    return render(request, "blog/category.html", context)
