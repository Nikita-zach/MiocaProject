from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Cart

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    context = {
        'cart': cart,
    }

    return render(request, 'cart.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Product removed from cart.')
    else:
        messages.error(request, 'Product not found in cart.')

    return redirect('cart')

