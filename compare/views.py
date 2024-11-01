from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import CompareItem
from product.models import Products

@login_required
def add_to_compare(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    compare_item, created = CompareItem.objects.get_or_create(user=request.user, product=product)

    if created:
        message = "Product has been added to compare list"
    else:
        message = "Product already added to compare list"

    return JsonResponse({'message': message})

def remove_from_compare(request, product_id):
    if request.method == "GET":
        product = get_object_or_404(Products, id=product_id)

        try:
            compare_item = CompareItem.objects.get(user=request.user, product=product)
            compare_item.delete()
            return JsonResponse({'message': 'Product removed from compare successfully!'})
        except CompareItem.DoesNotExist:
            return JsonResponse({'message': 'Product not found in compare list.'}, status=404)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)


def product_compare_view(request):
    products = Products.objects.filter(is_visible=True).order_by('sort')

    return render(request, 'compare.html', {'products': products})