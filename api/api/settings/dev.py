from .base import *

CORS_ORIGIN_ALLOW_ALL = True

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = "/media/"

STATICFILES_DIRS = (os.path.join(os.path.dirname(BASE_DIR), "static"),)
