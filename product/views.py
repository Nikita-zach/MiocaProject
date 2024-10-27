from .models import Products, Category,ProductImage, Review
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

def shop_view(request):
    categories = Category.objects.filter(is_visible=True).order_by('sort')

    selected_category_slug = request.GET.get('category', 'all')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', float('inf'))

    products_query = Products.objects.filter(is_visible=True)

    if selected_category_slug != 'all':
        products_query = products_query.filter(categories__slug=selected_category_slug)

    if min_price:
        products_query = products_query.filter(price__gte=min_price)
    if max_price and max_price != '0':
        products_query = products_query.filter(price__lte=max_price)

    products = products_query.distinct().order_by('sort')

    context = {
        'categories': categories,
        'products': products,
        'selected_category_slug': selected_category_slug,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'shop.html', context)

def product_detail_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    images = ProductImage.objects.filter(product=product)
    categories = product.categories.all()
    related_products = Products.objects.filter(categories__in=categories).exclude(id=product.id)[:4]  # Get 4 related products

    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else 0
    review_count = reviews.count()

    final_price = product.discount_price if product.discount_price else product.price
    discount_price = product.discount_price is not None

    context = {
        'product': product,
        'images': images,
        'categories': categories,
        'related_products': related_products,
        'average_rating': average_rating,
        'final_price': final_price,
        'discount_price': discount_price,
        'reviews': reviews,
        'review_count': review_count,
    }

    return render(request, 'single-product.html', context)
