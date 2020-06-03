from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email   = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    #creating custom field validation
    def clean_email(self,*args,**kwargs):  #clean_email is arbitory. But using the convention
        email = self.cleaned_data.get('email')
        print(email)
        if email.endswith(".edu"):
            raise forms.ValidationError("This is not a valid email.Dont use edu")
        return email
