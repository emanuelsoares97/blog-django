import tempfile
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from unittest.mock import patch, MagicMock
from allauth.socialaccount.models import SocialAccount
from users.signals import save_profile_picture_on_login
from users.models import Profile

User = get_user_model()

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SaveProfilePictureOnLoginSignalTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='googleuser', password='abc123')
        SocialAccount.objects.create(
            user=self.user,
            provider='google',
            extra_data={'picture': 'https://example.com/pic.jpg'}
        )
        # Ensure a Profile exists for this user
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.profile.image = None
        self.profile.save()


    @patch('requests.get')
    def test_saves_picture_when_not_exists(self, mock_requests_get):
        profile = self.user.profile

        # Mock the response from requests
        mock_response = MagicMock()
        mock_response.content = b'fake-image-data'
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        # Replace profile.image with a mock that has a .save() method
        mock_image = MagicMock()
        profile.image = mock_image

        # Call the signal function
        save_profile_picture_on_login(request=None, user=self.user)

        # Check that save was called once
        mock_image.save.assert_called_once()


    @patch('users.signals.requests.get')
    def test_does_not_overwrite_existing_google_image(self, mock_requests_get):
        """Ensure that an existing Google image is not overwritten."""
        profile = self.user.profile
        profile.image = MagicMock()
        profile.image.name = 'already_google.jpg'

        save_profile_picture_on_login(request=None, user=self.user)

        # Assert save was not called and requests.get was not called
        profile.image.save.assert_not_called()
        mock_requests_get.assert_not_called()

    @patch('users.signals.requests.get')
    def test_no_picture_in_extra_data(self, mock_requests_get):
        """Ensure that if extra_data has no picture, no download occurs."""
        social_account = self.user.socialaccount_set.first()
        social_account.extra_data = {}
        social_account.save()

        profile = self.user.profile
        profile.image = MagicMock()
        profile.image.name = None

        save_profile_picture_on_login(request=None, user=self.user)

        # Assert save was not called and requests.get was not called
        profile.image.save.assert_not_called()
        mock_requests_get.assert_not_called()
