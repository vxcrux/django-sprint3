from django.utils import timezone

from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category


def index(request):
    """Отображает главную страницу блога со списком последних публикаций"""
    now = timezone.now()

    posts_list = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).select_related(
        'author',
        'category',
        'location'
    ).order_by(
        '-pub_date'
    )[:5]

    context = {"posts": posts_list}
    return render(request, "blog/index.html", context)


def post_detail(request, id):
    """Отображает детальную страницу поста по его ID"""
    now = timezone.now()

    post = get_object_or_404(
        Post,
        pk=id,
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    )

    context = {"post": post}
    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):
    """Отображает страницу категории"""
    now = timezone.now()

    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts_list = Post.objects.filter(
        category=category,
        pub_date__lte=now,
        is_published=True
    ).select_related('author', 'location', 'category').order_by('-pub_date')

    context = {
        'category_slug': category_slug,
        'posts': posts_list,
        'category': category,
    }
    return render(request, "blog/category.html", context)
