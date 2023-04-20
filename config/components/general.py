'''General environment variables'''
from os         import path
from pathlib    import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LANGUAGE_CODE = 'ru-RU'

LOCALE_PATHS = ['movies/locale']

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = ()

MEDIA_URL = '/media/'
