from .base import *
from .drf_settings import *
from .celery_redis_settings import *


if eval(getenv('PRODUCTION').capitalize()):
    from .production import *
else:
    from .development import *
