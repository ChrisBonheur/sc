from django import forms

from store.models import Article

class ArticleForms(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('name', 'description', 'price_init', 'number', 
                'town', 'district', 'status', 'image_min', 'category'
                , 'delivery')

