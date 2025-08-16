from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Page
from blog.models import Post

User = get_user_model()

class UserViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123", email="test@test.com")
        self.user2 = User.objects.create_user(username="otheruser", password="otherpass123")
        # Cria posts de teste com campos válidos para o teu modelo Post
        for i in range(7):
            Post.objects.create(content=f"Conteúdo do post {i}", author=self.user)

    def test_login(self):
        url = reverse("login")
        data = {
            "login": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_logout(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("logout")
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_register_new_user_redirect(self):
        url = reverse('register')
        data = {
            "username": "Teste44",
            "email": "teste1@django.com",
            "password1": "Pass44StrongPassword123",
            "password2": "Pass44StrongPassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_register_new_user_form_display(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, 'Username')

    def test_register_new_user_invalid(self):
        url = reverse('register')
        data = {
            "username": "TesteErro",
            "email": "errado@django.com",
            "password1": "PassA123",
            "password2": "PassDifferent"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        form = response.context['form']
        self.assertFormError(form, 'password2', 'The two password fields didn’t match.')

    def test_profile_get_requires_login(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/login/?next={url}')

    def test_profile_get_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('u_form', response.context)
        self.assertIn('p_form', response.context)
        self.assertIn('posts', response.context)
        self.assertEqual(response.context['posts'].count(), 7)
        self.assertTrue(isinstance(response.context['posts'][0], Post))

    def test_profile_post_valid_update(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('profile')
        data = {
            'username': 'testuser',
            'email': 'newemail@test.com',
            # adiciona outros campos se necessário nos forms
        }
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        files = {'image': image}
        response = self.client.post(url, data=data, files=files, follow=True)
        self.assertRedirects(response, url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Your account has been updated!' in str(message) for message in messages))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@test.com')

    def test_profile_post_invalid_update(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('profile')
        data = {
            'username': '',  # inválido
            'email': 'invalidemail@test.com'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Error updating profile. Please try again.' in str(message) for message in messages))
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('u_form', response.context)
        self.assertIn('p_form', response.context)
        self.assertTrue(response.context['u_form'].errors)

    def test_public_profile_redirect_if_owner(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('public_profile', kwargs={'username': 'testuser'})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('profile'))

    def test_public_profile_for_other_user(self):
        url = reverse('public_profile', kwargs={'username': 'testuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/public_profile.html')
        self.assertIn('profile_user', response.context)
        self.assertEqual(response.context['profile_user'], self.user)
        self.assertIn('posts', response.context)
        self.assertTrue(hasattr(response.context['posts'], 'paginator'))
        self.assertTrue(hasattr(response.context['posts'], '__iter__'))
        self.assertTrue(response.context['is_paginated'])
        page_obj = response.context['page_obj']
        self.assertEqual(len(page_obj.object_list), 5)
        self.assertTrue(isinstance(page_obj, Page))
