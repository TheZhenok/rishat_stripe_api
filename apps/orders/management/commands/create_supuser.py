# Python
from datetime import datetime
from typing import Any

# Django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """Custom command for filling up database."""

    help = 'Custom command for create superuser up database.'

    def craete_superuser(self) -> None:

        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.cc",
            password="qwerty"
        )

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """Handles data filling."""

        start: datetime = datetime.now()
        self.craete_superuser()
        print(
            f'Created in: {(datetime.now()-start).total_seconds()} seconds'
        )