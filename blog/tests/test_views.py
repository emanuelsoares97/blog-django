from django.test import TestCase
from django.urls import reverse
from blog.models import Post, Comment
from django.contrib.auth import get_user_model


class BlogViewsTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass")
        self.client.login(username="tester", password="pass")
        self.post = Post.objects.create(author=self.user, content="Post Test")

    def test_homeblog_list(self):
        url = reverse('blog-home')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Destaques")

    def test_blog_home_listview(self):
        url = reverse('blog-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')


        context_posts = list(response.context['posts'])
        expected_posts = list(Post.objects.all().order_by('-created_at')[0:5])  # create pag
        self.assertListEqual(context_posts, expected_posts)

    def test_about(self):
        url = reverse('blog-about')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'blog/about.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sobre Este Blog")

    def test_get_new_post(self):
        url = reverse('post-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_post_new_post(self):
        url = reverse('post-create')
        data = {'content': 'Conteúdo do novo post'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='Conteúdo do novo post', author=self.user).exists())

    def test_update_post(self):
        url = reverse('post-update', args=[self.post.pk])
        data = {"content": "New content"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='New content', author=self.user).exists())
        self.assertRedirects(response, reverse('post-detail', args=[self.post.pk]))

    def test_update_post_anonymous_user(self):
        self.client.logout()
        url = reverse('post-update', args=[self.post.pk])
        data = {"content": "New content"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='Post Test', author=self.user).exists())

    def test_delete_post(self):
        url = reverse('post-delete', args=[self.post.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog-home'))

    def test_delete_post_as_different_user(self):
        User = get_user_model()
        other_user = User.objects.create_user(username="outro", password="senha")
        self.client.login(username="outro", password="senha")
        url = reverse('post-delete', args=[self.post.pk])
        response = self.client.post(url)

        self.assertNotEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_anonymous(self):
        self.client.logout()
        url = reverse('post-delete', args=[self.post.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_comment_post(self):
        self.client.logout()
        User = get_user_model()
        other_user = User.objects.create_user(username="outro", password="senha")
        self.client.login(username="outro", password="senha")
        url = reverse('add_comment', args=[self.post.pk])
        data = {"content": "Boa irmão!"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post-detail', args=[self.post.pk]))
        self.assertTrue(Comment.objects.filter(post=self.post, content="Boa irmão!", author=other_user).exists())
        detail_response = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertContains(detail_response, "Boa irmão!")


class ToggleLikeAjaxTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass")
        self.post = Post.objects.create(author=self.user, content="Test post")
        self.url = reverse('toggle-like-ajax', args=[self.post.pk])

    def test_toggle_like_post_ajax_authenticated(self):
        self.client.login(username="tester", password="pass")
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'liked': True, 'total_likes': 1}
        )
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'liked': False, 'total_likes': 0}
        )

    def test_toggle_like_post_ajax_anonymous(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_toggle_like_post_ajax_get_method_not_allowed(self):
        self.client.login(username="tester", password="pass")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
