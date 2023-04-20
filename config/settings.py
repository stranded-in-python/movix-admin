from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

base_settings = [
    'components/general.py',
    'components/django.py',
    'components/database.py',
]

include(*base_settings)
