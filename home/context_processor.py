from cart.models import Cart
from wishlist.models import Wishlist

def cart_items(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {
                'cart_items': cart.items.all(),
                'cart_item_count': cart.items.count(),
            }
        except Cart.DoesNotExist:
            return {
                'cart_items': [],
                'cart_item_count': 0,
            }
    return {
        'cart_items': [],
        'cart_item_count': 0,
    }

def wishlist_items(request):
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            return {
                'wishlist_items': wishlist.items.all(),
            }
        except Wishlist.DoesNotExist:
            return {
                'wishlist_items': [],
            }
    return {
        'wishlist_items': [],
    }
