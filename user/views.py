from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib import messages

from .forms import LoginForm, RegisterForm
from store.views import home
from .models import Profil
from communication.models import Message

def login_user(request):
    """Login user"""
    #if user login, no need to see login view
    if request.user.is_authenticated:
        return redirect('store:home')
    form = LoginForm(request.POST or None)
    error = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.add_message(request, messages.INFO, f'Content de vous voir {request.user} :)')
                return redirect('store:home')
            else:
                error = True
                content = 'ATTENTION ! Mot de passe ou nom d\'utilisateur invalide'
                messages.add_message(request, messages.ERROR, content)
    white_font = True    
    
    return render(request, 'user/login.html', locals())
        

def register(request):
    """Register new user"""
    #if user login, no need to see login view
    if request.user.is_authenticated:
        return redirect('store:home')
    form = RegisterForm(request.POST or None)
    email_exist = False
    username_exist = False 
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        check_email = User.objects.filter(email=email)
        check_username = User.objects.filter(username=username)
        if not check_email and not check_username:
            try:
                new_user = User.objects.create_user(username, email, password)
                user = User.objects.get(username=username)
                user_check = authenticate(username=user.username, password=password)
                login(request, user_check,  backend='django.contrib.auth.backends.ModelBackend')
            except Exception as e:
                print(e)
            else:
                messages.add_message(request, messages.SUCCESS, 'Votre compte a bien été crée !')
            
            return redirect('store:home')
        elif check_email:
            email_exist = True
        elif check_username:
            username_exist = True
    white_font = True
    
    return render(request, 'user/register.html', locals())

def auto_login(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    return render(request, 'user/auto_login.html', {})

@login_required
def profil(request):
    password_update_page = False
    if request.GET.get('password_update_page'):
        password_update_page = True
        
    context = {
        'gender_list': ['Homme', 'Femme', 'Autre'],
        'password_update_page': password_update_page
    }
    
    return render(request, 'user/profil.html', context)

@login_required
def logout_user(request):
    logout(request)
    return render(request, 'user/auto_login.html', {})

@login_required
def update(request):
    if request.GET.get('supprimer'):
        user = request.user
        user.is_active = False
        user.save()
        return redirect('store:home')

    if request.POST.get('new_password'):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user = request.user
        
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Mot de passe modifié !')
            auth = authenticate(username=user.username, password=new_password)
            login(request, auth)
            return redirect('store:home')
        else:
            content = 'ATTENTION ! Mot de passe invalide'
            messages.add_message(request, messages.ERROR, content)
            context = {
                'password_update_page': True,
            }
            return render(request, 'user/profil.html', context)   
          
    if request.POST.get('username'): 
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        new_password = request.POST.get('new_password')
        user_id = request.POST.get('user_id')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        mobile_money = request.POST.get('mobile_money')
        contact = request.POST.get('contact')
        
        user = User.objects.get(pk=user_id)
        print
        # user.first_name = first_name
        
        if email != user.email:
            try:
                User.objects.get(email=email)
            except:
                user.email = email
            else:
                error_email = True
        
        if username != user.username:
            try:
                User.objects.get(username=username)
            except:
                user.username = username
            else:
                error_username = True
            
        if first_name != user.first_name:
            user.first_name = first_name

        if last_name != user.last_name:
            user.last_name = last_name
        
        user.save()
        
        profil = Profil.objects.get_or_create(user=user)
        profil = Profil.objects.get(user=user)
        
        try:
            avatar_file = request.FILES['avatar']
        except:
            pass
        else:
            profil.avatar = avatar_file
            
        profil.gender = gender
        
        if contact != '':
            profil.contact = contact
        
        if mobile_money != '':
            profil.mobile_money = mobile_money
        
        profil.save()
        
        messages.add_message(request, messages.SUCCESS, 'Votre profil a été mis à jour!')
           
        return home(request)

    return redirect('user:profil')
