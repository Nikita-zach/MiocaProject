from django.shortcuts import render, redirect
from accounts.forms import NewUserCreationForm
from cart.models import Cart
from .forms import OrderForm


def checkout_view(request):
    cart = None
    order_items = []
    total_price = 0
    shipping_cost = 0

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        order_items = cart.items.all()
        total_price = sum(item.product.price * item.quantity for item in order_items)

        shipping_cost = 0 if total_price >= 39 else 9.00
        total_price += shipping_cost

        if request.method == "POST":
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.user = request.user
                order.total_price = total_price
                order.shipping_cost = shipping_cost
                order.save()
                return redirect('thank_you')
        else:
            order_form = OrderForm()

    else:
        if request.method == "POST":
            user_form = NewUserCreationForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
                return redirect('checkout')
        else:
            user_form = NewUserCreationForm()

    return render(request, 'checkout.html', {
        'order_items': order_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'user_form': user_form if not request.user.is_authenticated else None,
        'order_form': order_form if request.user.is_authenticated else None,
    })


def thank_you_view(request):
    return render(request, 'thank-you-page.html')