from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib import messages

from .forms import LoginForm, RegisterForm, ProfilForm, UserForm
from store.views import home
from .models import Profil, Gender
from communication.models import Message
from dashboard.models import Transaction

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
    user_instance = User.objects.get(pk=request.user.id)
    profil_instance, created = Profil.objects.get_or_create(user=request.user)
    
    user_form = UserForm(instance=user_instance)
    profil_form = ProfilForm(instance=profil_instance)
    
    if request.POST:
        user_form = UserForm(request.POST, instance=user_instance)
        if user_form.is_valid():
            user_form.save()

        profil_form = ProfilForm(request.POST, request.FILES, instance=profil_instance)
        profil = profil_form.save(commit=False)
        profil.save()
    elif request.GET.get('profil_id'):
        print("request found",request.GET.get('profil_id'))
        profil_id = request.GET.get('profil_id')
        profil = get_object_or_404(Profil, pk=profil_id)
        context =  {
            "profil": profil,
            "articles_selled_count_profil": Transaction.objects.filter(is_final=True, 
                                    invoice__seller_id=profil.user.id).count(),     
        }
        
        return render(request, 'user/profil-card.html', context)
            
    context = {
        'user_form': user_form,
        'profil_form': profil_form,
    }
    
    return render(request, 'user/profil.html', context)

@login_required
def logout_user(request):
    logout(request)
    return render(request, 'user/auto_login.html', {})

@login_required
def security(request):
    context = {}
    
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
            context['password_error'] = True
             
    return render(request, 'user/profil.html', context)  
