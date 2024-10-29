from django.shortcuts import render
from .models import ServiceSection, Stuff, Testimonials, BrandIcons, FAQ
from home.models import Feature

def about_page(request):
    service_section = ServiceSection.objects.first()
    features = Feature.objects.all()
    team = Stuff.objects.filter(is_visible=True).order_by('sort')
    testimonials = Testimonials.objects.all()
    brands = BrandIcons.objects.all()

    context = {
        'service_section': service_section,
        'features': features,
        'team': team,
        'testimonials': testimonials,
        'brands': brands,
    }
    return render(request, 'about.html', context)


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def privacy_policy(request):
    return render(request, 'privacy-policy.html')



