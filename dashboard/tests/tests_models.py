from django.test import TestCase
from django.contrib.auth.   models import User

from dashboard.models import Invoice, Order
from store.models import Article
from store.tests.tests_views import create_article
 
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
        decline an order's article
        """
        #get an order
        #make a request http with "decliner-la-commande" inside and order_id
        #assert(order.article.available, False)
        pass
        