import tempfile
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from allauth.socialaccount.models import SocialAccount
from users.signals import save_profile_picture_on_login
from users.models import Profile

User = get_user_model()


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SaveProfilePictureOnLoginSignalTest(TestCase):
    def setUp(self):
        # create a user and related social account (google) with a picture url
        self.user = User.objects.create_user(username="googleuser", password="abc123")
        SocialAccount.objects.create(
            user=self.user,
            provider="google",
            extra_data={"picture": "https://example.com/pic.jpg"},
        )
        # ensure a Profile exists and starts without an image
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.profile.image = None
        self.profile.save(update_fields=["image"])

    @patch("users.signals.cld_upload")
    def test_saves_picture_when_not_exists(self, mock_cld_upload):
        """
        when profile has no image, it should upload the google picture and assign the public_id
        """
        # arrange: mock cloudinary upload response
        mock_cld_upload.return_value = {
            "public_id": "profile_pictures/googleuser_google",
            "secure_url": "https://res.cloudinary.com/dogevu6ip/image/upload/v123/profile_pictures/googleuser_google.jpg",
        }

        # act
        save_profile_picture_on_login(request=None, user=self.user)

        # assert: uploader called once with the expected args
        mock_cld_upload.assert_called_once()
        args, kwargs = mock_cld_upload.call_args
        assert args[0] == "https://example.com/pic.jpg"
        assert kwargs["public_id"] == "profile_pictures/googleuser_google"
        assert kwargs["folder"] == "profile_pictures"
        assert kwargs["overwrite"] is True
        assert kwargs["resource_type"] == "image"

        # the profile image should now point to the returned public_id
        self.profile.refresh_from_db()
        # CloudinaryField should expose public_id from assigned value
        assert getattr(self.profile.image, "public_id", None) == "profile_pictures/googleuser_google"

    @patch("users.signals.cld_upload")
    def test_does_not_overwrite_existing_google_image(self, mock_cld_upload):
        """
        ensure that an existing image is not overwritten on subsequent logins
        """
        # arrange: simulate an existing cloudinary image
        self.profile.image = "profile_pictures/googleuser_google"
        self.profile.save(update_fields=["image"])

        # act
        save_profile_picture_on_login(request=None, user=self.user)

        # assert: no new upload and the public_id remains unchanged
        mock_cld_upload.assert_not_called()
        self.profile.refresh_from_db()
        assert getattr(self.profile.image, "public_id", None) == "profile_pictures/googleuser_google"

    @patch("users.signals.cld_upload")
    def test_no_picture_in_extra_data(self, mock_cld_upload):
        """
        if extra_data has no picture, no upload must occur
        """
        # arrange: remove picture from extra_data
        sa = self.user.socialaccount_set.first()
        sa.extra_data = {}
        sa.save(update_fields=["extra_data"])

        # act
        save_profile_picture_on_login(request=None, user=self.user)

        # assert: uploader not called and profile image remains empty
        mock_cld_upload.assert_not_called()
        self.profile.refresh_from_db()
        assert not getattr(self.profile.image, "public_id", None)
