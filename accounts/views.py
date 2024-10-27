from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import NewUserCreationForm

def login_register_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")

        elif 'register' in request.POST:
            form = NewUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login_register')
            else:
                messages.error(request, "Please correct the errors below.")
    else:
        form = NewUserCreationForm()

    return render(request, 'login.html', {
        'login_form': None,
        'register_form': form,
        'messages': messages.get_messages(request),
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payments.models import Order
from .forms import AccountUpdateForm

@login_required
def account_dashboard(request):
    orders = Order.objects.filter(user=request.user)

    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
            return redirect('account_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountUpdateForm(instance=request.user)

    context = {
        'orders': orders,
        'user': request.user,
        'form': form
    }
    return render(request, 'my-account.html', context)
