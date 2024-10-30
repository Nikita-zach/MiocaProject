from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    context = {
        'cart': cart,
    }

    return render(request, 'cart.html', context)


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        cart_item.delete()
    return redirect('cart')
