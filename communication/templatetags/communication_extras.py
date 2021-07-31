from django import template
from django.contrib.auth.models import User

from communication.models import ChatMessage

register = template.Library()

@register.filter
def message_talk_count(current_user, talk):
    """return count message of a current user in a talk"""
    return ChatMessage.objects.filter(talk=talk, delivred=False)\
        .exclude(talk__chats__user=current_user).count()

@register.filter
def other_user(curent_user, talk):
    """get user who's not the connected user"""
    if curent_user.id == talk.user1_id:
        other_user_id = talk.user2_id
    else:
        other_user_id = talk.user1_id
    
    return User.objects.get(pk=other_user_id)