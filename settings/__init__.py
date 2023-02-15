# Python
from typing import (
    Any, 
    Type,
)
from decouple import config

# Django
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(env_variable: str, type: Type) -> Any:
    try:
        return config(env_variable, cast=type)
    except KeyError:
        raise ImproperlyConfigured(
            f'Set {env_variable} environment variable'
        )
