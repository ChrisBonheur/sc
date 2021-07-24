from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from dashboard.models import Invoice, Order
from store.models import Article
from store.tests.tests_views import create_article
from communication.models import NotifMessage
 
class SignalsTestCase(TestCase):
    """Test all signals about store app"""     
    def setUp(self):
        self.user = User.objects.create_user(username="exo", password="123456")
        self.article = create_article("radio", self.user)
        self.order = Order.objects.create(customer=self.user, article=self.article)
    
    def test_decrement_quanity_article(self):
        """test decrementation quanity of article"""
        article = create_article("clavier", self.user, town="bz", status="neuf")
        art_number_before = article.number
        order = Order.objects.create(customer=self.user, article=article)
        art_number_after = Article.objects.get(name=article).number
        self.assertEqual(art_number_before - 1, art_number_after)
    
    def test_notif_send_to_seller_after_ordering(self):
        article = create_article("clavier", self.user, town="bz", status="neuf")
        notif_count_before = NotifMessage.objects.count()
        Order.objects.create(customer=self.user, article=article)
        notif_count_after = NotifMessage.objects.count()
        self.assertEqual(notif_count_after, notif_count_before + 1)
        

