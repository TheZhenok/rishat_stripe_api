# Python
from typing import Optional

# Django
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

# Local
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    """Admin panel for Item."""

    model = Item

    fieldsets = (
        ('Information', {
            'fields': (
                'name',
                'description',
            )
        }),
        ('Permissions', {
            'fields': (
                'price',
            )
        }),
    )
    readonly_fields = ()
    list_display = (
        'name',
        'price',
    )

    def get_readonly_fields(
        self, 
        request: WSGIRequest, 
        obj: Optional[Item] = ...
    ) -> tuple:
        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'price',
        )

admin.site.register(Item, ItemAdmin)
