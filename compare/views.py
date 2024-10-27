from django.shortcuts import render
from product.models import Products


def product_compare_view(request):
    products = Products.objects.filter(is_visible=True).order_by('sort')

    return render(request, 'compare.html', {'products': products})