from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            register_form = UserCreationForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Error. Invalid login or password.")
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            login_form = AuthenticationForm()
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('home')
            else:
                messages.error(request, "Error. Invalid username or password.")
    else:
        login_form = AuthenticationForm()
        register_form = UserCreationForm()

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'login.html', context)