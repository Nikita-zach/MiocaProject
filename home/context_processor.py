from cart.models import Cart
from wishlist.models import Wishlist


def wishlist_and_cart(request):
    wishlist_items = []
    cart_items = []

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        cart_items = Cart.objects.filter(user=request.user)

    return {
        'wishlist_items': wishlist_items,
        'cart_items': cart_items,
    }
