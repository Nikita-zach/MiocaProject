from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Products
from .models import Wishlist, WishlistItem

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.items.all()
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    wishlist_item, item_created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

    if not item_created:
        messages.info(request, f'{product.name} is already in your wishlist.')
    else:
        messages.success(request, f'Added {product.name} to your wishlist.')

    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product_id=product_id)

    wishlist_item.delete()
    messages.success(request, f'Removed {wishlist_item.product.name} from your wishlist.')

    return redirect('wishlist')
