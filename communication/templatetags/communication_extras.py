from django import template
from django.contrib.auth.models import User

from communication.models import MessageText

register = template.Library()

@register.filter
def message_count(current_user, talk):
    """return count message of a current user in a talk"""
    return MessageText.objects.filter(talk=talk, recipient=current_user, seen=False).count()


@register.filter
def other_user(curent_user, talk):
    """get user who's not the connected user"""
    if curent_user.id == talk.user1_id:
        other_user_id = talk.user2_id
    else:
        other_user_id = talk.user1_id
    
    return User.objects.get(pk=other_user_id)