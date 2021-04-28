from django import forms
from .models import happy_blog


class HappyBlogForm(forms.ModelForm):
    class Meta:
        model = happy_blog
        fields = ('name', 'job_type', 'tweet', 'image', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.TextInput(attrs={'class': 'form-control'}),
        }
