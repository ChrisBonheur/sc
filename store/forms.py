from django import forms

from store.models import Article

class ArticleForms(forms.ModelForm):
    class Meta:
        ATTRS_DATA = {"class": "form-control border-0 border-bottom border-secondary"}
        model = Article
        fields = ('name', 'description', 'price_init', 'number', 
                'town', 'district', 'status', 'image_min', 'category'
                , 'delivery')
        widgets = {
            'name': forms.TextInput(attrs=ATTRS_DATA),
            'description': forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
            'price_init': forms.NumberInput(attrs=ATTRS_DATA),
            'number': forms.NumberInput(attrs=ATTRS_DATA),
            'town': forms.Select(attrs=ATTRS_DATA),
            'district': forms.TextInput(attrs=ATTRS_DATA),
            'status': forms.Select(attrs=ATTRS_DATA),
            'image_min': forms.FileInput(attrs=ATTRS_DATA),
            'category': forms.Select(attrs=ATTRS_DATA),
            'delivery': forms.CheckboxInput(attrs={"class": "w-50 h-50"}),
        }

