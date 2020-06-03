from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .forms import BlogPostModelForm
from .models import BlogPost

# GET -> returns 1 object
# filter = takes a list of objects also called queryset


"""def blog_post_detail_page(request,slug): #to pass id dynamically
    #queryset = BlogPost.objects.filter(slug=slug)
    #if queryset.count == 0:
    #    raise Http404
    #obj = queryset.first()   # it will render first object
    obj = get_object_or_404(BlogPost,slug=slug)

    template_name = 'blog_post_detail.html'
    context = {'object':obj}   #{'title' : obj.title}, To print object
    return render(request,template_name,context)"""

# CRUD -> Create,Retrieve,Update,Delete
#GET -> Retrieve/list
#Post -> Create,Update,Delete
#now creating seperate methods for crud operations

def blog_post_list_view(request):   #list_view is a version of retrieve_view
#list out objects
#could also work as 'search'

    #now = timezone.now()
    qs = BlogPost.objects.all().published() #custom queryset #queryset -> List of python objects
    #qs = BlogPost.objects.filter(publish_date__lte=now) #lse -> less than or equal to
    #gse could also be used. Instead of this we will use django model manager to list published item.

    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs|my_qs).distinct()  #will prevent duplicate posts to show
    template_name = 'blog/list.html'
    context = {'object_list' : qs}
    return render(request,template_name,context)


#@login_required
#check seasions before running the view if user is logged in or not
@staff_member_required
#this is another decorator which will only allow staff members. We can also use both decorators together.
def blog_post_create_view(request):
#used to create objects -> using forms
    form = BlogPostModelForm(request.POST or  None, request.FILES or None)  #passing BlogPostForm in view
    if form.is_valid():
        obj = form.save(commit = False) #commit = False will not make save yet
    #    obj.title = form.cleaned_data.get("title") + "0"    #manupulating data
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()   #to re-initilize the form


    template_name = 'form.html'
    context = {'form' : form}
    return render(request,template_name,context)


@staff_member_required
def blog_post_detail_view(request,slug): #or retrieve_view
# 1 object -> detail view. same as list_view but it returns only 1 object.
    obj = get_object_or_404(BlogPost,slug=slug) #using blog_post_detail_page entirely.
    template_name = 'blog/detail.html'
    context = {"object":obj}
    return render(request,template_name,context)


@staff_member_required
def blog_post_update_view(request,slug):
    obj = get_object_or_404(BlogPost,slug=slug) #using blog_post_detail_page entirely.
    form = BlogPostModelForm(request.POST or  None, instance=obj)
    # passing instance is needed to make update happen.
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"title": f"update{obj.title}", 'form' : form}
    #updating title by fstring substitution
    return render(request,template_name,context)


@staff_member_required
def blog_post_delete_view(request,slug):
    obj = get_object_or_404(BlogPost,slug=slug) #using blog_post_detail_page entirely.
    template_name = 'blog/delete.html'
    if request.method  == 'POST':
        obj.delete()
        return redirect("/blog")    #redirecting to blog posts after deletion
    context = {'object':obj}
    return render(request,template_name,context)
