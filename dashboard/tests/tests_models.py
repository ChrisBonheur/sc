from django.test import TestCase
from django.contrib.auth.   models import User

from dashboard.models import Invoice, Order
from store.tests.tests_views import create_article
 
class SignalsTestCase(TestCase):
    """Test all signals about store app"""
    def setUp(self):
        self.user = User.objects.create_user(username="exo", password="123456",\
            email="exo@gmail.com")
    def test_upload_manage(self):
        """test if order's attribut manage become True
        when invoice is created for this order
        """
        user = self.user
        article = create_article()
        #create order
        order = Order.objects.create(
            user=user,
            article=article,
        )
        #create invoice
        invoice = Invoice.objects.create(order=order)
        order = Order.objects.get(article=article)
        msg = "Signal not send to order to upload manage attribut to False"
        self.assertEqual(order.manage, True, msg=msg)
    
    def test_uplod_article_available(self):
        """test that article.available is False when seller or article.user
        decline an order's article
        """
        pass
        