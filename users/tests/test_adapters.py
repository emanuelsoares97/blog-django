from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from users.adapters import MySocialAccountAdapter

class FakeSocialLogin:
    """Classe de apoio para simular sociallogin."""
    def __init__(self, email):
        self.account = type('obj', (object,), {'extra_data': {'email': email}})
        self.state = {}
        self.connected_user = None
    def connect(self, request, user):
        self.connected_user = user

class SocialAccountAdapterTest(TestCase):
    def setUp(self):
        self.adapter = MySocialAccountAdapter()
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='existente', email='exemplo@dominio.com')

    def test_pre_social_login_user_exists(self):
        request = self.factory.get('/')
        sociallogin = FakeSocialLogin('exemplo@dominio.com')
        self.adapter.pre_social_login(request, sociallogin)
        self.assertEqual(sociallogin.connected_user, self.user)
        self.assertEqual(sociallogin.state['process'], 'login')

    def test_pre_social_login_user_does_not_exist(self):
        request = self.factory.get('/')
        sociallogin = FakeSocialLogin('naoexiste@dominio.com')
        self.adapter.pre_social_login(request, sociallogin)
        self.assertIsNone(sociallogin.connected_user)
        self.assertNotIn('process', sociallogin.state)
