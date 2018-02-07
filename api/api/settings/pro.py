from .base import *

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = ()

DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = from_env("USGV_EMAIL_HOST")
EMAIL_HOST_PASSWORD = from_env("USGV_EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = from_env("USGV_EMAIL_HOST_USER")

MEDIA_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), "static")

