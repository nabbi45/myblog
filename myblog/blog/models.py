from django.conf import settings
from django.db import models
from django.db.models import Q #for complex lookups
from django.utils import timezone


User = settings.AUTH_USER_MODEL #this is needed whenever we use user.

class BlogPostQuerySet(models.QuerySet):
    def published(self):    #this is arbitory
        now = timezone.now()
        return self.filter(publish_date__lte=now) #this is not arbitory
        #this working as BlogPost.objects.all() with filter

    def search(self, query):
        lookup = (
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(user__email__icontains=query) |
                    Q(user__username__icontains=query)

                    )

        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self.db)

    def published(self):
        self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


class BlogPost(models.Model):   #blogpost_set.all() ->  will give all the queryset related to user.
    #id = models.IntegerField()  by default. Also known as PK
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    #To associate a post to that user. 1 is superuser here.
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    # it will automatically create image folder in media folder.
    title = models.CharField(max_length = 120)
    slug = models.SlugField(unique=True)   #to make url readable after slash
    #ex. 127.0.0.1:8000/blog/getting-started. hello world -> becomes hello-world
    content = models.TextField(null = True, blank = True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ['-pk','-publish_date','-updated','-timestamp']    #to show newest first

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
