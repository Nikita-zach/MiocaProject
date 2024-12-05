from cart.models import Cart
from wishlist.models import Wishlist
from django.conf import settings


def cart_items(request):
    """
    Context processor that adds the current user's cart items to the context.
    - If the user is authenticated, it attempts to retrieve the user's cart and
      its items from the database.
    - If the cart does not exist, it returns an empty cart with zero item count.
    - If the user is not authenticated, it returns an empty cart with zero item count.

    Args:
        request (HttpRequest): The HTTP request object, containing the user's session data.

    Returns:
        dict: A dictionary containing 'cart_items' (list of items in the cart) and
              'cart_item_count' (the number of items in the cart).

    Example:
        - If the user is authenticated and has items in their cart, the function
          will return a dictionary with a list of items and the count.
        - If the user is not authenticated, the function will return an empty list
          and a count of zero.
    """
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
    """
    Context processor that adds the current user's wishlist items to the context.
    - If the user is authenticated, it attempts to retrieve the user's wishlist
      from the database.
    - If the wishlist does not exist, it returns an empty wishlist.
    - If the user is not authenticated, it returns an empty wishlist.

    Args:
        request (HttpRequest): The HTTP request object, containing the user's session data.

    Returns:
        dict: A dictionary containing 'wishlist_items' (list of items in the wishlist).

    Example:
        - If the user is authenticated and has items in their wishlist, the function
          will return a dictionary with a list of items.
        - If the user is not authenticated, the function will return an empty list.
    """
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

def global_texts(request):
    """
    Context processor to provide dynamic text configurations to all templates.

    This context processor is used to inject a dictionary of pre-defined,
    dynamic texts (stored in `settings.DYNAMIC_TEXTS`) into the template
    context. It allows developers to centralize and manage all text-related
    content for the project, ensuring consistency and ease of updates.

    Parameters:
    -----------
    request : HttpRequest
        The HTTP request object passed automatically by Django.

    Returns:
    --------
    dict
        A dictionary containing the `DYNAMIC_TEXTS` defined in settings,
        accessible globally in templates.
    """
    return {
        'DYNAMIC_TEXTS': settings.DYNAMIC_TEXTS,
    }
