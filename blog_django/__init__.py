import cloudinary

from django.conf import settings

cloudinary.config(
cloud_name=settings.CLOUDINARY_STORAGE["CLOUD_NAME"],
api_key=settings.CLOUDINARY_STORAGE["API_KEY"],
api_secret=settings.CLOUDINARY_STORAGE["API_SECRET"],
secure=True,
)