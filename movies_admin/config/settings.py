import os

from pathlib import Path
from split_settings.tools import include
from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')


# Application definition

include(
    '../components/definition.py',
)

# Database

include(
    '../components/database.py',
)

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

include(
    '../components/validation.py',
)

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

include(
    '../components/internationalization.py',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG:
    import mimetypes
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    mimetypes.add_type("application/javascript", ".js", True)
