from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
import re

from store.models import Article
from .models import Message, Talk, MessageText


@login_required
def new_msg(request):
    if request.GET.get('talk_id'):
        talk = get_object_or_404(Talk, pk=request.GET.get('talk_id'))
        
        if talk.user1_id == request.user.id:
            user2_id = talk.user2_id
        else:
            user2_id = talk.user1_id
            
    elif request.GET.get('article_id'):
        article = get_object_or_404(Article, pk=request.GET.get('article_id'))
        user2_id = article.user.id 
        try:
            #select query
            #verification if curent user and seller user are often a talk
            q1 = (Q(user1_id=request.user.id) | Q(user2_id=request.user.id))
            q2 = (Q(user1_id=article.user.id) | Q(user2_id=article.user.id))
            talk = Talk.objects.get(Q(q1) & Q(q2))
        except:
            #if they are not a talk, creating of a talk
            talk = Talk.objects.create(user1_id=request.user.id, user2_id=article.user.id)
    else:
        redirect('communication:box_msg')
    
    if request.POST:
        message = request.POST.get('message')
        #set of regex to filtre message and remove any form number
        regex ='^.*(([0-9] ?){9,}).*'
        regex = re.match(regex, message)
        try:
            regex.group(1)
        except:
            pass
        else:
            message = message.replace(regex.group(1), '" "')
        
        #creating for new message
        try:
            new_message = MessageText.objects.create(
                content=message,
                recipient_id=user2_id,
                sender_id=request.user.id,
                talk=talk
            )
            messages.add_message(request, messages.SUCCESS, 'Message envoyé !')
            talk.last_message_date = timezone.now()
            talk.save()
            
        except Exception as e:
            print(e)
        else:
            print('message create')
    

    #make readed all message receive by current user
    for message in MessageText.objects.filter(recipient=request.user, seen=False):
        message.seen = True
        message.save()
    
    context = {
        'message_list': MessageText.objects.filter(talk=talk),
        'talk': talk,
    }
    return render(request, 'communication/new_message.html', context)

@login_required
def box_msg(request):
    if request.POST:
        #create for new mail
        pass
    
    context = {
        'talks': Talk.objects.filter(Q(user1_id=request.user.id) | Q(user2_id=request.user.id)),
    }
    return render(request, 'communication/box_message.html', context)

@login_required
def notifications(request):
    context = {
        'notifs': Message.objects.filter(Q(type_msg='notif') & Q(recipient_id=request.user.id))
    }
    return render(request, 'communication/notifications.html', context)

@login_required
def notif_detail(request):
    notif_id = request.GET.get('notif_id')
    notif = get_object_or_404(Message, pk=notif_id)
    link = notif.link
    notif.readed = True
    notif.save()
    
    return redirect(link)