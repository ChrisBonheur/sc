from django import forms
from .models import Order

class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'article')

