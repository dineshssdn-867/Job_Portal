from django import forms
from .models import blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = blog
        fields = ('name', 'title', 'tweet', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
