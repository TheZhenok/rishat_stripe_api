# Python
from typing import Optional

# Django
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

# Local
from .models import (
    Item,
    Order,
    Discount,
)


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
                'currency',
            )
        }),
    )
    readonly_fields = ()
    list_display = (
        'name',
        'price',
        'currency',
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


class OrderAdmin(admin.ModelAdmin):

    model = Order


class DiscountAdmin(admin.ModelAdmin):

    model = Discount


admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Discount, DiscountAdmin)
