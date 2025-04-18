import os
from .base import *

django_env = os.getenv('DJANGO_ENV', 'development')

if django_env == 'development':
    from .dev import *
elif django_env == 'production':
    from .prod import *
else:
    raise ValueError("Invalid DJANGO_ENV specified. Use 'development' or 'production'.")
