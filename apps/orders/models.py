# Python
from typing import Optional
import datetime

# Django
from django.db import models
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist
)
from django.conf import settings

# Stripe
import stripe


class ItemManager(models.Manager):
    """Manager for item."""

    def get_if_exist(
        self, 
        id: int
    ) -> Optional['Item']:

        try:
            return self.get(id=id)
        except ObjectDoesNotExist:
            return None


class Item(models.Model):
    """Model for Stripe."""

    MAX_PRICE = 999
    MIN_PRICE = 0

    name = models.CharField(
        verbose_name="имя",
        max_length=200
    )
    description = models.TextField(
        verbose_name="описание"
    )
    price = models.DecimalField(
        verbose_name="цена",
        max_digits=6,
        decimal_places=2
    )
    objects = ItemManager()

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self) -> str:
        return f"{self.name} | {self.price}$"

    def save(self, *args, **kwags) -> None:
        self.full_clean()
        return super().save( *args, **kwags)

    def get_stripe_id(
        self
    ) -> Optional[stripe.checkout.Session]:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': self.amount / 1000,
                            'product_data': {
                                'name': self.name,
                                'description': self.description
                            }
                        },
                        'quantity': 1
                    },
                ],
                mode='payment',
                success_url=settings.DOMAIN + '/success',
                cancel_url=settings.DOMAIN + '/cancel',
            )
        except Exception as e:
            print(
                '----------------------',
                (
                    f'[{datetime.datetime.now()} ERROR] '
                    f'Stripe exeption by item id {self.id}'
                ),
                e,
                '----------------------',
                sep='\n'
            )
            return None

        return checkout_session

    def clean(self) -> None:
        if (
            not self.price
        ) or (
            self.price <= self.MIN_PRICE
        ) or (
            self.price >= self.MAX_PRICE
        ):
            raise ValidationError(
                (
                    f"The price cannot be equal to or less than zero or grand than {self.MAX_PRICE}! | "
                    f"Цена не может быть равна или меньше нуля или больше {self.MAX_PRICE}!"
                )
            )
            
        return super().clean()

    @property
    def amount(self) -> int:
        return int(self.price * 100)
