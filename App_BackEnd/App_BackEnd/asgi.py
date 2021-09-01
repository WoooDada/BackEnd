import os
import django
from channels.routing import get_default_application
from channels.routing import ProtocolTypeRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE","App_BackEnd.settings")
django.setup()

application = get_default_application()