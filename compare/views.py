from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from product.models import Products

@login_required
def add_to_compare(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    compare_list = request.session.get('compare_list', [])

    if str(product.id) not in compare_list:
        compare_list.append(str(product.id))
        request.session['compare_list'] = compare_list
        message = "Product has been added to compare list"
    else:
        message = "Product already added to compare list"

    return JsonResponse({'message': message})

@login_required
def remove_from_compare(request, product_id):
    if request.method == "GET":
        product = get_object_or_404(Products, id=product_id)

        compare_list = request.session.get('compare_list', [])

        if str(product.id) in compare_list:
            compare_list.remove(str(product.id))
            request.session['compare_list'] = compare_list
            return JsonResponse({'message': 'Product removed from compare successfully!'})
        else:
            return JsonResponse({'message': 'Product not found in compare list.'}, status=404)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)


def product_compare_view(request):
    products = Products.objects.filter(is_visible=True).order_by('sort')

    return render(request, 'compare.html', {'products': products})