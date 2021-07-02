from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings

from .models import Profil, Gender

BASE_DIR = settings.BASE_DIR

class LoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="coco", password="123456")

    def setUp(self):
        self.user = User.objects.get(username="coco")

    def test_login_view_200(self):
        """test if login view return 200"""
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_user(self):
        """Test to login user"""
        user = self.user
        data = {"username":user.username,"password":"123456"}
        response = self.client.post(reverse('user:login'), data)
        self.assertRedirects(response, reverse('store:home'))

    def test_redirect_in_login_view(self):
        """Test redirection to login view while form not valid"""
        data = {"username":"not_exists", "password":"not_exists"}
        response = self.client.post(reverse('user:login'), data)
        self.assertEqual(response.status_code, 200)

class RegisterViewTestCase(LoginViewTestCase):
    def test_acces_to_registre_page(self):
        """test that register page return 200"""        
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        """test to register a new user"""
        user_count_before = User.objects.count()
        data = {"username": "boby", "email": "boby@gmail.com",\
                "password":"123456", "confirm_password": "123456"}
        self.client.post(reverse('user:register'), data)
        user_count_after= User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)

    def test_register_view_return_200_while_bad_data(self):
        """test return 200 if user send bad data to login"""
        data = {"username": "not_exist"}
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

class UpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="name_test", password="123")
        self.client.login(username="name_test", password="123")
        
    def test_access_update_profil_view(self):
        """test if access update page return 200"""
        user = self.user
        response = self.client.get(reverse('user:profil'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_is_update(self):
        """test user update"""
        user =self.user
        data = {
            'username': "chris",
            'mtn_money': "068314433",
            'avatar': File(open(f'{BASE_DIR}/user/static/user/img_test/v3.jpeg', 'rb')),
            'gender': Gender.objects.create(sexe='Masculin').id,
            'contact_mtn': "068314433",
            'contact_airtel': "068314433",
            "whatsap_number": " 068314433",
            "airtel_money": "068314433",
        }
        response = self.client.post(reverse('user:profil'), data)
        user = User.objects.get(pk=user.id)
        self.assertNotEqual(user.username, "name_test")
        profil = Profil.objects.get(user=user)
        self.assertEqual(profil.mtn_money, '068314433')
    
    def test_deactive_user(self):
        """test user can deactive his account"""
        user = User.objects.create_user(username="bnhr", password="123456")
        self.client.login(username=user, password="123456")
        self.client.get(reverse('user:update'), {"supprimer": user})
        user_login = self.client.login(username=user, password="123456")
        self.assertFalse(user_login)

