from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category

POSTS_PER_PAGE_ON_INDEX = 5


def get_base_posts_queryset():
    """Возвращает список с базовыми фильтрами и select_related"""
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related(
        'author',
        'category',
        'location'
    )


def index(request):
    """Отображает главную страницу блога со списком последних публикаций"""
    context = {"posts": get_base_posts_queryset()[:POSTS_PER_PAGE_ON_INDEX]}
    return render(request, "blog/index.html", context)


def post_detail(request, post_id):
    """Отображает детальную страницу поста по его ID"""
    post = get_object_or_404(
        get_base_posts_queryset(),
        pk=post_id
    )

    context = {"post": post}
    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):
    """Отображает страницу категории"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    context = {
        'posts': get_base_posts_queryset().filter(category=category),
        'category': category,
    }
    return render(request, "blog/category.html", context)
