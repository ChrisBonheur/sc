from django.db import models
from django.contrib.auth.models import User
# from django.db.models import Q
# from django.conf import settings

from store.models import Article

class Talk(models.Model):
    user_one = models.IntegerField(null=True)
    user_two = models.IntegerField(null=True)
    date_last_message_added = models.DateTimeField(auto_now_add=True, null=True)
    article = models.ForeignKey(Article, related_name="talks",
                                on_delete=models.CASCADE, null=True)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    delivred = models.BooleanField(default=False)

    class Meta:
        abstract = True
        
class ChatMessage(Message):
    talk = models.ForeignKey(Talk, related_name="chats",
                             on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content
    
class NotifMessage(Message):
    def __str__(self):
        return self.content

# def curent_user():
#     return settings.AUTH_USER_MODEL
    
# class Message(models.Model):
#     TYPE_MSG_CHOICES = models.TextChoices('notif', 'message')
#     content = models.TextField()
#     recipient_id = models.IntegerField(verbose_name='Recevreur')
#     type_msg = models.CharField(max_length=100, choices=TYPE_MSG_CHOICES.choices,\
#          default='notif')
#     date_send = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'envoie')
#     readed = models.BooleanField(default=False)
#     link = models.CharField(max_length=500, null=True)
    
#     class Meta:
#         verbose_name = "Message"
#         ordering = ('-date_send',)

# class Talk(models.Model):
#     user1_id = models.IntegerField()
#     user2_id = models.IntegerField()
#     last_message_date = models.DateTimeField(auto_now_add=True, null=True)
    
#     class Meta:
#         verbose_name = "Conversation"
#         ordering = ('-last_message_date',)
        
#     @property
#     def user1(self):
#         return User.objects.get(pk=self.user1_id)

#     @property
#     def user2(self):
#         return User.objects.get(pk=self.user2_id)    
        
# class MessageText(models.Model):
#     sender_id = models.IntegerField()
#     recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     content = models.TextField()
#     date = models.DateTimeField(auto_now_add=True, null=True)
#     seen = models.BooleanField(default=False)
#     talk = models.ForeignKey(Talk, related_name='messages', \
#         on_delete=models.SET_NULL, null=True)
#     alert_play = models.BooleanField(default=False)
    
#     class Meta:
#         verbose_name = 'Message texte'
#         ordering = ('date',)
    
#     def __str__(self):
#         return self.content
 
    