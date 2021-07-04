from django import forms
import re

from .models import Order

class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'article')
        
class MomoNumber(forms.Form):
    DATA_ATTRS = {"class": "form-control input-number", "placeholder": "+242"}
    mtn_account_number = forms.IntegerField(required=False)
    confirm_number_mtn = forms.IntegerField(required=False)
    airtel_account_number = forms.IntegerField(required=False)
    confirm_number_airtel = forms.IntegerField(required=False)
    
    mtn_account_number.widget.attrs.update(DATA_ATTRS)
    confirm_number_mtn.widget.attrs.update(DATA_ATTRS)
    airtel_account_number.widget.attrs.update(DATA_ATTRS)
    confirm_number_airtel.widget.attrs.update(DATA_ATTRS)

    
    
    

