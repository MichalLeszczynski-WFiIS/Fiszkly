from fiszkly.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "hcnuvw0@0v@8g&cr-5-ujsvnx=)0nz&k51m#&u9r)dn7_44fro"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
