from django.test import TestCase
from django.contrib.auth.   models import User
from django.shortcuts import reverse

from dashboard.models import Invoice, Order
from store.models import Article
from store.tests.tests_views import create_article
from communication.models import Message
 
class SignalsTestCase(TestCase):
    """Test all signals about store app"""     
    def setUp(self):
        self.user = User.objects.create_user(username="exo", password="123456")
        self.article = create_article("radio", self.user)
        self.order = Order.objects.create(user=self.user, article=self.article)
            
    def test_upload_manage(self):
        """test if order's attribut manage become True
        when invoice is created for this order
        """
        invoice = Invoice.objects.create(order=self.order)
        order = Order.objects.get(article=self.article)
        msg = "Signal not send to order to upload manage attribut to False"
        self.assertEqual(order.manage, True, msg=msg)
    
    

