from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Products
from .models import Wishlist, WishlistItem

@login_required
def wishlist_view(request):
    """
    Displays the current user's wishlist page.

    - Retrieves or creates a wishlist for the authenticated user.
    - Lists all products added to the user's wishlist.

    Context:
        wishlist_items (QuerySet): List of items in the user's wishlist.

    Template:
        wishlist.html: Template for rendering the wishlist page.
    """
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.items.all()
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    """
    Adds a product to the user's wishlist.

    - If the product is already in the wishlist, an info message is shown.
    - Otherwise, the product is added, and a success message is shown.

    Parameters:
        product_id (int): The ID of the product to add.

    Messages:
        Success: If the product was successfully added.
        Info: If the product is already in the wishlist.

    Redirect:
        Redirects the user back to the wishlist page.
        :param product_id:
        :param request:
    """
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
    """
    Removes a product from the user's wishlist.

    - If the product exists in the wishlist, it is removed, and a success message is shown.

    Parameters:
        product_id (int): The ID of the product to remove.

    Messages:
        Success: If the product was successfully removed.

    Redirect:
        Redirects the user back to the wishlist page.
        :param product_id:
        :param request:
    """
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, wishlist=wishlist, product_id=product_id)

    wishlist_item.delete()
    messages.success(request, f'Removed {wishlist_item.product.name} from your wishlist.')

    return redirect('wishlist')
