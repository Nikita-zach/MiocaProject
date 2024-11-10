from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogWindow, BlogSection, Comment


def blog_detail(request, blog_id):
    blog_section = BlogSection.objects.get(id=blog_id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Comment.objects.create(blog_section=blog_section, name=name, email=email, message=message)
        return redirect('blog_detail', blog_section_id=blog_section.id)

    context = {
        'blog_section': blog_section,
    }
    return render(request, 'blog-single.html', context)


def blog_list_view(request, blog_window_id):
    blog_window = get_object_or_404(BlogWindow, id=blog_window_id)

    context = {
        'blog_window': blog_window,
    }

    return render(request, 'blog-search.html', context)

def add_comment(request, blog_id):
    if request.method == "POST":
        blog_section = get_object_or_404(BlogSection, id=blog_id)
        name = request.POST.get('name')
        message = request.POST.get('message')

        comment = Comment(blog_section=blog_section, name=name, message=message)
        comment.save()

        return redirect('blog_detail', blog_id=blog_id)

    return HttpResponse(status=400)
