from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
import re

from store.models import Article
from .models import Message, Talk, ChatMessage


@login_required
def chat_message(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    
    #get or create talk
    try:
        q1 = (Q(user_one=request.user.id) | Q(user_two=request.user.id))
        q2 = (Q(user_one=article.user.id) | Q(user_two=article.user.id))
        talk = Talk.objects.get(Q(q1) & Q(q2) & Q(article=article))
    except Exception as e:
        talk = Talk.objects.create(article=article, user_one=request.user.id,
                                    user_two=article.user.id)
    
    if request.POST.get('message'):
        message = request.POST.get('message')
        #find and remove number tel if existe in message
        regex_number_phone ='^.*(([0-9] ?){9}).*$'
        regex_number_phone = re.match(regex_number_phone, message)
        
        if regex_number_phone is not None:
            message = message.replace(regex_number_phone.group(1), '" "')

        new_chat = ChatMessage.objects.create(user=request.user, content=message, talk=talk)

    #make delivred to True for all messages receive by current user
    for message in ChatMessage.objects.filter(talk=talk).exclude(user=request.user):
        message.delivred = True
        message.save()
    
    context = {
        'message_list': ChatMessage.objects.filter(talk=talk),
        'article': article,
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