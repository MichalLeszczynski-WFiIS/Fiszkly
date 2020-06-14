from fiszkly.settings.common import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ["fiszkly.pl"]
SECURE_REFERRER_POLICY = "same-origin"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Options listed below require an SSL certificate
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
