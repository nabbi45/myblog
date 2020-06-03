from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
    my_title = "Hello there...."
    qs = BlogPost.objects.all()[:5]
    context = {"title": "Welcome to MyBlog", "blog_list" : qs}
    return render(request, "home.html", context)

def about_page(request):
    about = "about page..."
    return render(request,"about.html",{'title':about})

def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)

        form = ContactForm()    #to re-initilize form after submit

    context = {
            'title':"contact us",
            'form':form
    }
    return render(request,"form.html",context)
