from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(label="", max_length=100)
    email = forms.EmailField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="", widget=forms.PasswordInput)
    
    username.widget.attrs.update({'placeholder': 'Nom d\'utilisateur'})
    email.widget.attrs.update({'placeholder': 'Email'})
    password.widget.attrs.update({'placeholder': 'Mot de passe', 'class': 'inputForm'})
    confirm_password.widget.attrs.update({'placeholder': 'Confirmer mot de passe', 'class': 'inputForm'})
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        
        if confirm_password != self.cleaned_data['password']:
            raise forms.ValidationError('Les mots de passes diffèrent !')
        
        return confirm_password
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        try:
            User.objects.get(email=email)
        except:
            forms.ValidationError("Cet email existe déjà, vous connectez")
        
        return email
           
class LoginForm(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)
    
    username.widget.attrs.update({'placeholder': 'Nom d\'utilisateur'})
    password.widget.attrs.update({'placeholder': 'Mot de passe', 'class': 'inputForm'})
             