from django import forms
from .models import BlogPost

# storing the data in database by django-form
class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):   #model forms
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug','content','publish_date']

    def clean_title(self,*args,**kwargs):  #clean_email is arbitory. But using the convention
        title = self.cleaned_data.get('title')
        instance = self.instance
        print(instance)
        qs = BlogPost.objects.filter(title__iexact=title)
        #title__iexact will also give error if we use capital letter in title that had been used.
        # if you want title case sensitive then use title instead of title__iexact.
        if instance is not None:
            qs=qs.exclude(pk=instance.pk) #same as id = instance.id
            #it prevent same validation error as creating new blog_post_create_view
        if qs.exists(): #can also use unique class in models to achieve this.
            raise forms.ValidationError("This title has already been used")
        return title
