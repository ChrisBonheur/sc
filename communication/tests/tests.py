from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Message, Talk

class NewMessageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="chris", password="123", email="chris@gmail.com")
        user2 = User.objects.create_user(username="dan", password="1234", email="dan@gmail.com")
        talk = Talk.objects.create(user1_id=user1.id, user2_id=user2.id)
    
    def setUp(self):
        self.user1 = User.objects.get(username="chris")
        self.user2 = User.objects.get(username="dan")
        self.client.login(username="chris", password="123")
        self.logged_get = lambda url_name, data: self.client.get(reverse(url_name), data)
        self.logged_post = lambda url_name, data: self.client.post(reverse(url_name), data)
        self.talk = Talk.objects.get(user1_id=self.user1.id, user2_id=self.user2.id)
        
    def test_acces_to_page_for_new_message(self):
        talk_id = self.talk.id
        response = self.logged_get('communication:new_msg', {"talk_id": talk_id})
        
        self.assertEqual(response.status_code, 200)
