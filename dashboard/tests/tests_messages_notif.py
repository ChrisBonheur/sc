from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from store.tests.tests_views import create_article
from communication.models import Message
from dashboard.models import Order
from dashboard.messages_info import article_delete_success

class MessageNotifTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='davel', 
                                             password="123456")
        self.article = create_article("clavier", self.user)
        self.order = Order.objects.create(user=self.user, article=self.article)
        self.client.login(username=self.user, password="123456")
        
    def test_success_delete_article(self):
        """test message info success deleting is added after deleting of an
        article"""
        article = self.article
        self.client.get(reverse('dashboard:delete'), {"article_id": article.id})
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertContains(response, article_delete_success(article))
    
    def test_success_update_article(self):
        """test message info succes update is added after
        update action"""
        article = self.article
        attributs = ["price_init", "district", "delivery", "number", "description", "image_min"]
        data_article = {attr: getattr(article, attr) for attr in attributs}
        data_article["name"] = "clavier azerty"
        data_article["town"] = article.town.id
        data_article["status"] = article.status.id
        data_article["category"] = article.category.id
        self.client.post(reverse('dashboard:update', args=(article.id,)), data_article)
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertContains(response, article_update_success(data_article["name"]))
        
    def test_send_notifs_valid_order(self):
        """Test send notification when ordering is valided"""
        order = self.order
        msg_count_before = Message.objects.filter(recipient_id=order.user.id).count()
        response = self.client.get(reverse("dashboard:invoices"), {"order_id": order.id, \
            "valider-la-commande": order.article})
        #test notif sended to custommer when seller valid an order
        msg_count_after = Message.objects.filter(recipient_id=self.order.user.id).count()
        err_msg = "Message not send to a customer for order validation by seller"
        self.assertEqual(msg_count_before + 1, msg_count_after, msg=err_msg)