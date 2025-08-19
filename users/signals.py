import logging
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from allauth.account.signals import user_logged_in
from cloudinary.uploader import upload as cld_upload

from .models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """create a Profile when a new User is created"""
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(user_logged_in)
def save_profile_picture_on_login(request, user, **kwargs):
    """
    first google login: grab google profile picture url and upload directly to cloudinary
    - ensure Profile exists (get_or_create)
    - only set image if it's empty (first-time only)
    - use a stable public_id (profile_pictures/<username>_google)
    """
    try:
        logger.info("[avatar] login user=%s", getattr(user, "username", "<no-username>"))

        # get the google social account
        sa = user.socialaccount_set.filter(provider="google").first()
        if not sa:
            logger.info("[avatar] no google socialaccount for user=%s", user.username)
            return

        extra = sa.extra_data or {}
        pic = extra.get("picture") or extra.get("picture_url")
        logger.info("[avatar] picture_from_google=%s", pic)
        if not pic:
            logger.info("[avatar] no picture in extra_data for user=%s", user.username)
            return

        # normalize to https just in case
        if pic.startswith("http://"):
            pic = pic.replace("http://", "https://", 1)

        # ensure we have a Profile
        profile, _ = Profile.objects.get_or_create(user=user)

        # if it already has an image, don't touch it (first login only)
        has_file = bool(getattr(profile.image, "public_id", None) or getattr(profile.image, "name", ""))
        if has_file:
            logger.info("[avatar] image already set for user=%s; skip", user.username)
            return

        # upload directly to cloudinary using the remote url
        # stable public_id avoids duplicates; folder is redundant but ok
        public_id = f"profile_pictures/{user.username}_google"
        logger.info("[avatar] cloudinary upload start public_id=%s", public_id)
        res = cld_upload(
            pic,
            public_id=public_id,
            folder="profile_pictures",
            overwrite=True,
            resource_type="image",
        )
        pid = res.get("public_id")
        secure_url = res.get("secure_url")
        logger.info("[avatar] cloudinary upload done pid=%s url=%s", pid, secure_url)

        if not pid:
            logger.error("[avatar] cloudinary returned no public_id for user=%s", user.username)
            return

        # assign the Cloudinary public_id to the CloudinaryField
        profile.image = pid
        if hasattr(profile, "image_from_google"):
            profile.image_from_google = True
            profile.save(update_fields=["image", "image_from_google"])
        else:
            profile.save(update_fields=["image"])

        logger.info("[avatar] saved google avatar for user=%s public_id=%s", user.username, pid)

    except Exception as e:
        logger.error("[avatar] error user=%s: %s", getattr(user, "username", "<no-username>"), e)
