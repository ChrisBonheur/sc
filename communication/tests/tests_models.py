from django.test import TestCase
from django.contrib.auth.models import User

from communication.models import Talk, ChatMessage, NotifMessage
from store.tests.tests_views import create_article

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bnhr", password="123")
        self.article = create_article()
        
    def test_talk_created(self):
        article = self.article
        talk_count_before = Talk.objects.count()
        Talk.objects.create(article=article, user_one=article.user.id, 
                            user_two=self.user.id)
        talk_count_after = Talk.objects.count()
        self.assertEqual(talk_count_before + 1, talk_count_after)
    
    def test_chat_message_create(self):
        user = self.user
        talk = Talk.objects.create(article=self.article)
        chat_msg_count_before = ChatMessage.objects.count()
        ChatMessage.objects.create(user=user, content="salut", talk=talk)
        chat_msg_count_after = ChatMessage.objects.count()
        self.assertEqual(chat_msg_count_before + 1, chat_msg_count_after)
        
    def test_notif_message_create(self):
        user = self.user
        notif_msg_count_before = NotifMessage.objects.count()
        NotifMessage.objects.create(user=user, content="salut")
        notif_msg_count_after = NotifMessage.objects.count()
        self.assertEqual(notif_msg_count_before + 1, notif_msg_count_after)
        