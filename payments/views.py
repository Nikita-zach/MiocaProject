from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.defaultfilters import first

from home.admin import ThankYouImageAdmin
from .models import Order, ThankYouImage
from .forms import ShippingForm, OrderForm
from django.contrib.auth.decorators import login_required
from cart.models import Cart

@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)

    shipping_cost = Decimal(0) if total_price >= Decimal(39) else Decimal(9.00)
    final_total_price = total_price + shipping_cost

    shipping_form = ShippingForm()
    order_form = OrderForm()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'final_total_price': final_total_price,
        'shipping_form': shipping_form,
        'order_form': order_form
    })


@login_required
def place_order(request):
    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        order_form = OrderForm(request.POST)
        if shipping_form.is_valid() and order_form.is_valid():
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            total_price = Decimal(sum(item.total_price() for item in cart_items))
            shipping_cost = Decimal(0) if total_price >= Decimal(39) else Decimal(9.00)
            final_total_price = total_price + shipping_cost

            Order.objects.create(
                user=request.user,
                status='PENDING',
                total_quantity=sum(item.quantity for item in cart_items),
                total_price=final_total_price
            )

            cart.items.all().delete()

            messages.success(request, "Your order has been placed successfully!")
            return redirect('thank_you')

        else:
            messages.error(request, "Please correct the errors in the form.")
            return redirect('checkout')

    return redirect('checkout')


def thank_you_view(request):
    thank_you = ThankYouImage.objects.first()
    return render(request, 'thank-you-page.html',{'thank_you':thank_you})