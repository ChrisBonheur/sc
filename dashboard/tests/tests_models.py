from django.test import TestCase
from django.contrib.auth.   models import User
from django.shortcuts import reverse

from dashboard.models import Invoice, Order
from store.models import Article
from store.tests.tests_views import create_article, PASSWORD
 
class SignalsTestCase(TestCase):
    """Test all signals about store app"""
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="exo", password="123456",\
            email="exo@gmail.com")
        article = create_article("radio")
        order = Order.objects.create(
            user=user,
            article=article,
        )        
    def setUp(self):
        self.user = User.objects.get(username="exo")
        self.article = Article.objects.get(name="radio")
        self.order = Order.objects.get(article=self.article)
            
    def test_upload_manage(self):
        """test if order's attribut manage become True
        when invoice is created for this order
        """
        user = self.user
        article = self.article
        #create order
        order = self.order
        #create invoice
        invoice = Invoice.objects.create(order=order)
        order = Order.objects.get(article=article)
        msg = "Signal not send to order to upload manage attribut to False"
        self.assertEqual(order.manage, True, msg=msg)
    
    def test_uplod_article_available(self):
        """test that article.available is False when seller or article.user
        decline an order's article (action realised by a middleware)
        """
        #get an order
        order = self.order
        #make a request http with "decliner-la-commande" inside and order_id
        self.client.login(username="exo", password="123456")
        self.client.get(reverse('dashboard:orders'), {"decliner-la-commande": order.article, \
            "order_id": order.id})
        article = Article.objects.get(name="radio")
        #assert(order.article.available, False)
        err_msg = "Article has been decline but available attribut not upload to False"
        self.assertEqual(article.available, False, msg=err_msg)
        
    def test_send_notifs(self):
        """Test many notif send to customer"""
        order = self.order
        customer = order.user
        seller = order.article.user
        #login seller
        self.client.login(username=seller, password=PASSWORD)
        res_seller = self.client.get(reverse("dashboard:invoices"), {"order_id": order.id, \
            "valider-la-commande": order.article})
        #test seller receive a valid notif
        self.assertContains(res_seller, 'Commande validée avec succès')
        #test notif sended to custommer when seller valid an order
        #request http with order_id args and valider-la-commande args
        #assert(response, order_accepted_msg)
    