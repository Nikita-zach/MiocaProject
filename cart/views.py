from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Products
from .models import Cart, CartItem


@login_required
def cart_view(request):
    """
    Displays the user's shopping cart, showing the products added, their quantities, and the total price.

    The view retrieves the user's cart and calculates the total price of the items in the cart.
    It then renders the cart page with a list of products, their quantities, and the total price.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the "cart.html" template with the user's cart items and total price.

    Example:
        A logged-in user visits their cart page to see their added products and total cost.
    """

    cart, created = Cart.objects.get_or_create(user=request.user)

    products = []
    total_price = 0

    for item in cart.items.all():
        products.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item.product.final_price * item.quantity
        })
        total_price += item.product.final_price * item.quantity

    context = {
        'cart': products,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    """
    Adds a product to the user's cart. If the product is already in the cart, it increments the quantity by 1.

    If the product is not already in the cart, it is added with a quantity of 1.
    A success message is displayed after the item is added.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponse: Redirects the user back to the cart page with a success message.

    Example:
        A user adds a product to their cart and is redirected to the cart page with a success message.
    """
    product = get_object_or_404(Products, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    """
    Removes a product from the user's cart. If the quantity is greater than 1, it decrements the quantity by 1.
    If the quantity is 1, the product is completely removed from the cart.

    A success message is displayed after the item is removed or its quantity is decreased.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to remove from the cart.

    Returns:
        HttpResponse: Redirects the user back to the cart page with a success message.

    Example:
        A user removes an item from their cart and is redirected to the cart page with a success message.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f'Removed one {cart_item.product.name} from your cart. {cart_item.quantity} items left.')
    else:
        cart_item.delete()
        messages.success(request, f'{cart_item.product.name} has been removed from your cart.')

    return redirect('cart')

@login_required
def clear_cart(request):
    """
    Clears all items from the user's shopping cart.

    This view deletes all `CartItem` objects associated with the user's cart, effectively emptying the cart.
    After clearing the cart, the user is redirected back to the cart page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects the user back to the cart page after clearing the cart.

    Example:
        A user clears their cart and is redirected to an empty cart page.
    """
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    return redirect('cart')