from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Article

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Article
        fields = '__all__'
