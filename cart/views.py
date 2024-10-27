from django.shortcuts import render
from .models import Cart

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    context = {
        'cart': cart,
    }

    return render(request, 'cart.html', context)
