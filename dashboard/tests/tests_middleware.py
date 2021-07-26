from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from store.tests.tests_views import create_article
from store.models import Article
from dashboard.models import Order
from communication.models import NotifMessage

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="belvy", password="123456")
        self.client.login(username=self.user, password="123456")
        self.article = create_article("vélo", self.user)
        self.order = Order.objects.create(customer=self.user, article=self.article)
        
    def test_number_increment(self):
        """test when ordering is cancel by customer, article number
        increment to 1"""
        order = self.order
        article = self.article
        article_number_before = article.number
        self.client.get(f'{reverse("dashboard:orders")}', {"annuler-la-commande": article,\
            "order_id": order.id}) 
        article = Article.objects.get(name=order.article)
        article_number_after = article.number
        self.assertEqual(article_number_before + 1, article_number_after)
    
    def test_uplod_article_available(self):
        """test that article.available is False when seller or article.user
        decline an order's article (action realised by a middleware)
        """
        #get an order
        order = self.order
        #make a request http with "decliner-la-commande" inside and order_id
        self.client.get(reverse('dashboard:orders'), {"decliner-la-commande": order.article, \
            "order_id": order.id})
        article = Article.objects.get(name=order.article)
        #assert(order.article.available, False)
        err_msg = "Article has been decline but available attribut not upload to False"
        self.assertEqual(article.available, False, msg=err_msg)
    
    def test_notif_send_to_customer(self):
        """notif is sent to customer if ordering is validated by seller"""
        order = self.order
        notifs_count_before = NotifMessage.objects.count()
        self.client.get(f"{reverse('dashboard:orders')}", {"order_id": order.id, 
                                        "valider-la-commande": order.article})
        notifs_count_after = NotifMessage.objects.count()
        self.assertEqual(notifs_count_after, notifs_count_before + 1)
    
    def test_notif_send_to_customer(self):
        """notif is sent to customer if ordering is decline by seller"""
        order = self.order
        notifs_count_before = NotifMessage.objects.count()
        self.client.get(f"{reverse('dashboard:orders')}", {"order_id": order.id, 
                                        "decliner-la-commande": order.article})
        notifs_count_after = NotifMessage.objects.count()
        self.assertEqual(notifs_count_after, notifs_count_before + 1)
        
    def test_notif_deleted(self):
        """Test notif sent to seller when customer pass an ordering is deleted
        if customer cancel this ordering
        """
        notif_count_before = NotifMessage.objects.count()
        order =self.order
        self.client.get(f'{reverse("dashboard:orders")}', {"annuler-la-commande": order.article,\
            "order_id": order.id}) 
        notif_count_after = NotifMessage.objects.count()
        self.assertEqual(notif_count_after, notif_count_before - 1)
        
        