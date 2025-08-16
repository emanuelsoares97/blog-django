import tempfile
import shutil
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from unittest.mock import patch, MagicMock
from allauth.socialaccount.models import SocialAccount
from users.signals import save_profile_picture_on_login

User = get_user_model()

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SaveProfilePictureOnLoginSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='googleuser', password='abc123')
        self.social_account = SocialAccount.objects.create(
            user=self.user,
            provider='google',
            extra_data={'picture': 'https://example.com/pic.jpg'}
        )

    @patch('requests.get')
    def test_saves_picture_when_not_exists(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.content = b'fake-image-data'
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        profile = self.user.profile
        profile.image.delete(save=True)  # Limpa qualquer imagem para simular "sem imagem"
        save_profile_picture_on_login(request=None, user=self.user)
        profile.refresh_from_db()
        expected_prefix = f"{self.user.username}_google"
        self.assertIn(expected_prefix, profile.image.name,
                      f"Nome real da imagem: {profile.image.name!r}")

    @patch('requests.get')
    def test_does_not_overwrite_existing_google_image(self, mock_requests_get):
        profile = self.user.profile
        profile.image.save('already_google.jpg', ContentFile(b'dadosantigos'), save=True)
        old_content = profile.image.file.read()

        save_profile_picture_on_login(request=None, user=self.user)
        profile.refresh_from_db()
        self.assertEqual(profile.image.read(), old_content)
        mock_requests_get.assert_not_called()

    @patch('requests.get')
    def test_no_picture_in_extra_data(self, mock_requests_get):
        social_account = self.user.socialaccount_set.first()
        social_account.extra_data = {}
        social_account.save()

        profile = self.user.profile
        profile.image.delete(save=True)
        save_profile_picture_on_login(request=None, user=self.user)
        profile.refresh_from_db()
        self.assertFalse(profile.image)
        mock_requests_get.assert_not_called()
