from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Wishlist, WishlistItem
from product.models import Products
from django.http import JsonResponse


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if created:
        message = "Product has been added to Wishlist"
    else:
        message = "Product is already added to Wishlist"

    return JsonResponse({'message': message})

def remove_from_wishlist(request, product_id):
    if request.method == "GET":
        product = get_object_or_404(Products, id=product_id)
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product=product)
            wishlist_item.delete()
            return JsonResponse({'message': 'Product removed from wishlist successfully!'})
        except Wishlist.DoesNotExist:
            return JsonResponse({'message': 'Product not found in wishlist.'}, status=404)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist = get_object_or_404(Wishlist, user=request.user)
    else:
        wishlist = None

    context = {
        'wishlist': wishlist
    }

    return render(request, 'wishlist.html', context)
