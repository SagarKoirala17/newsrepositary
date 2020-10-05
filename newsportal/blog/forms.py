from django import forms
from .models import Blog
from .models import Category

class BlogForm(forms.ModelForm):
    #title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'title'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Blog
        fields = '__all__'
        exclude=['title']