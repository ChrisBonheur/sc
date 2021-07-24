from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from communication.models import Talk, ChatMessage, NotifMessage
from store.tests.tests_views import create_article

class NewMsgTestCase(TestCase):
    def setUp(self):
        self.article = create_article()
        self.user = User.objects.create_user(username="bnhr", password="123")
        self.client.login(username=self.user, password="123")
        
    def test_access_list_msg_page(self):
        article = self.article
        user = self.user
        response = self.client.get(reverse('communication:chat_message', 
                                           args=(article.id,)))
        self.assertEqual(response.status_code, 200)
    
    def test_send_new_msg(self):
        article = self.article
        message_count_before = ChatMessage.objects.count()
        msg = "Hello world"
        response = self.client.post(reverse('communication:chat_message',args=(article.id,)),
                                                             {"message": msg})
        message_count_after = ChatMessage.objects.count()
        self.assertEqual(message_count_before + 1, message_count_after)
        #test messages are showing in template
        self.assertContains(response, msg)
        
    def test_number_phone_is_automitical_deleted(self):
        article = self.article
        phone_number = "05 582 49 25"
        msg = f"Hello my number is {phone_number}"
        response = self.client.post(reverse('communication:chat_message', args=(article.id,)), 
                                    {"message": msg})
        self.assertNotContains(response, phone_number)

class NotifMessageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bnhr",
                                             password="123")
        self.client.login(username="bnhr", password="123")
        
    def test_access_notif_page(self):
        user = self.user
        response = self.client.get(reverse('communication:notifications'))
        self.assertEqual(response.status_code, 200)
    
    def test_notif_link_redirection(self):
        """test to get one notification link redirection"""
        notif = NotifMessage.objects.create(
            user=self.user,
            content="hello world",
            link=reverse('store:favourite'),
        )
        response  = self.client.get(reverse('communication:notifications'), 
                                    {"notif_id": notif.id})
        self.assertRedirects(response, notif.link)
        #test notif become delivred notif
        notif = NotifMessage.objects.get(pk=notif.id)
        self.assertTrue(notif.delivred)