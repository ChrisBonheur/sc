from django import forms
from .models import Order

class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'article', 'availabilty', 'manage', 'price_ttc')

