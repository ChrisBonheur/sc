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
    
    def clean(self):
        cleaned_data =  super(MomoNumber, self.clean())
        mtn_account_number = cleaned_data.get('mtn_account_number')
        confirm_number_mtn = cleaned_data.get('confirm_number_mtn')
        airtel_account_number = cleaned_data.get('airtel_account_number')
        confirm_number_airtel = cleaned_data.get('confirm_number_airtel')
        
        if (not mtn_account_number or not confirm_number_mtn) and \
            (not airtel_account_number or not confirm_number_airtel):
                raise forms.ValidationError("Vous devez renseigner au moins un numéro d'un compte electronique")
        elif mtn_account_number != confirm_number_mtn or airtel_account_number != confirm_number_airtel:
            raise forms.ValidationError("Attention les numéros diffèrent, veuillez vérifier SVP")
        elif re.match("^(242)?06[0-9]{7}$", mtn_account_number) is None:
            raise forms.ValidationError("Ceci n'est pas un numéro MTN")
        elif re.match("^(242)?05[0-9]{7}$", airtel_account_number) is None:
            raise forms.ValidationError("Ceci n'est pas un numéro Airtel")
        
        return cleaned_data
    
    
    

