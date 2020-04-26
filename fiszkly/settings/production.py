from fiszkly.settings.common import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['77.55.214.25']
SECURE_REFERRER_POLICY = "no-referrer"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Options listed below require a SSL certificate
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
