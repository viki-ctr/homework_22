from django.core.cache import cache

from .models import Product


def get_products_by_category(category_slug):
    cache_key = f'products_category_{category_slug}'
    products = cache.get(cache_key)

    if not products:
        products = Product.objects.filter(
            category__slug=category_slug,
            is_published=True
        ).select_related('category')
        cache.set(cache_key, products, 60 * 60)
    return products


def get_all_products():
    cache_key = 'all_products_list'
    products = cache.get(cache_key)

    if not products:
        products = Product.objects.filter(
            is_published=True
        ).select_related('category')
        cache.set(cache_key, products, 60 * 30)
    return products