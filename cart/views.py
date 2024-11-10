from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Products
from .models import Cart, CartItem


@login_required
def cart_view(request):
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
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    return redirect('cart')