from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from private_messages.models import Message
from private_messages.forms import MessageForm
from django.utils import timezone
import json

User = get_user_model()

class PrivateMessagesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')


        self.msg1 = Message.objects.create(
            sender=self.user2, recipient=self.user1,
            content="Hello user1!", timestamp=timezone.now(), read=False
        )

        self.msg2 = Message.objects.create(
            sender=self.user1, recipient=self.user2,
            content="Hi user2!", timestamp=timezone.now(), read=True
        )

    def test_inbox_requires_login(self):
        url = reverse('inbox')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/login/?next={url}')

    def test_inbox_shows_contacts_with_unread_count(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('inbox')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'private_messages/inbox.html')
        contacts = response.context['contacts']

        self.assertIn(self.user2, contacts)

        user2_contact = contacts.get(pk=self.user2.pk)
        self.assertEqual(user2_contact.unread_count, 1)

    def test_conversation_requires_login(self):
        url = reverse('conversation', kwargs={'username': self.user2.username})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/login/?next={url}')

    def test_conversation_get(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('conversation', kwargs={'username': self.user2.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'private_messages/conversation.html')
        self.assertIn('messages', response.context)
        self.assertIn('form', response.context)
        self.assertIn('other_user', response.context)
        self.assertIn('current_username', response.context)

        self.msg1.refresh_from_db()
        self.assertTrue(self.msg1.read)

    def test_conversation_post_valid_form_redirect(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('conversation', kwargs={'username': self.user2.username})
        data = {'content': 'Nova mensagem!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, url)  

        new_msg = Message.objects.filter(sender=self.user1, recipient=self.user2, content='Nova mensagem!').first()
        self.assertIsNotNone(new_msg)

    def test_conversation_post_valid_form_ajax(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('conversation', kwargs={'username': self.user2.username})
        data = {'content': 'Mensagem AJAX!'}
        response = self.client.post(url, data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.content)
        self.assertEqual(resp_data['sender'], self.user1.username)
        self.assertEqual(resp_data['content'], 'Mensagem AJAX!')
        self.assertIn('timestamp', resp_data)

    def test_conversation_post_invalid_form(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('conversation', kwargs={'username': self.user2.username})
        data = {'content': ''}  # inválido, campo obrigatório
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # re-renderiza
        self.assertTemplateUsed(response, 'private_messages/conversation.html')
        form = response.context['form']
        self.assertTrue(form.errors)
