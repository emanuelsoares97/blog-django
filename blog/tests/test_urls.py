from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog import views

class TestBlogUrls(SimpleTestCase):

    def test_blog_home_url_resolves(self):
        url = reverse('blog-home')
        self.assertEqual(resolve(url).func.view_class.__name__, 'PostListView')

    def test_blog_about_url_resolves(self):
        url = reverse('blog-about')
        self.assertEqual(resolve(url).func, views.about)


    def test_post_create_url_resolves(self):
        url = reverse('post-create')
        self.assertEqual(resolve(url).func.view_class.__name__, 'PostCreateView')

    def test_toggle_like_ajax_url_resolves(self):
        url = reverse('toggle-like-ajax', args=[1])
        self.assertEqual(resolve(url).func, views.toggle_like_post_ajax)
