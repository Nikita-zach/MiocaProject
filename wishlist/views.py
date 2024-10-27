from django.shortcuts import render, get_object_or_404
from .models import Wishlist


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist = get_object_or_404(Wishlist, user=request.user)
    else:
        wishlist = None

    context = {
        'wishlist': wishlist
    }

    return render(request, 'wishlist.html', context)
