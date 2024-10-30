from django.shortcuts import render,redirect, get_object_or_404
from .models import Wishlist
from product.models import Products

def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
        wishlist_item.delete()
    return redirect('wishlist')


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist = get_object_or_404(Wishlist, user=request.user)
    else:
        wishlist = None

    context = {
        'wishlist': wishlist
    }

    return render(request, 'wishlist.html', context)
