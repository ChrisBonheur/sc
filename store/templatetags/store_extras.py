from django import template
from django.utils import timezone

from store.models import Favourite

register = template.Library()

@register.filter
def calcul_date(date_time):
    """This function calcul and return time since article has benn added"""
    date_calcul = timezone.now() - date_time
    if date_calcul.days <= 0:
        if date_calcul.seconds < 60:
            return f'{date_calcul.seconds}s'
        elif date_calcul.seconds >= 60 and date_calcul.seconds < 3600:
            minute = int(date_calcul.seconds / 60)
            return f'{minute}min'
        else:
            hour = int(date_calcul.seconds / 3600)
            return f'{hour}hr'
    else:
        if date_calcul.days < 30:
            days = date_calcul.days
            indication = 'jr'
            if days > 1:
                indication = 'jrs'
            return f'{date_calcul.days}{indication}'
        if date_calcul.days >= 30 and date_calcul.days < 360:
            month = int(date_calcul.days / 30)
            return f'{month}mois'
        else:
            year = int(date_calcul.days / 360)
            indication = 'an'
            if year > 1:
                indication = 'ans'
            return f'{year}{indication}'
        
@register.filter
def is_favourite(user, article):
    """test if article is in user favourite"""
    try:
        Favourite.objects.get(user=user).articles.get(pk=article.id)
    except Exception:
        return False
    else:
        return True