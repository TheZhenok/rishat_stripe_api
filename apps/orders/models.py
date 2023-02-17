# Python
from typing import (
    Optional, 
    Any, 
)
import datetime
from functools import cached_property

# Django
from django.db import models
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist
)
from django.conf import settings
from django.db.models import (
    QuerySet,
    Sum,
)
from django.core.validators import MaxValueValidator

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
    CURRENCY_PATTERN = (
        ("usd", "USD"),
        ("eur", "EUR"),
    )

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
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_PATTERN
    )
    objects = ItemManager()

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self) -> str:
        return f"{self.name} | {self.price}" + (
            "$" if (
                self.currency == "usd"
            ) else "€"
        )

    def save(self, *args, **kwags) -> None:
        self.full_clean()
        return super().save( *args, **kwags)

    def get_stripe_dict(
        self, 
        list_items: list[dict]
    ) -> list[dict]:

        tax_list: list[int] = []
        taxs: QuerySet[Tax] = Tax.objects.filter(
            id=self.id
        )

        tax: Tax
        for tax in taxs:
            stripe_tax = stripe.TaxRate.create(
                display_name=tax.display_name,
                inclusive=tax.inclusive,
                percentage=tax.percentage,
                country=tax.country,
                description=tax.description,
            )
            tax_list.append(stripe_tax.id)

        if not hasattr(self, '_data_obj'):
            self._data_obj: dict = {
                'price_data': {
                    'currency': self.currency,
                    'unit_amount': self.amount,
                    'product_data': {
                        'name': self.name,
                        'description': self.description
                    },
                },
                'quantity': 0,
                'tax_rates': tax_list
            }
        else:
            index: int = list_items.index(self._data_obj)
            list_items.pop(index)

        self._data_obj['quantity'] += 1
        list_items.append(self._data_obj)
        return list_items

    def get_stripe_session(
        self, 
        line_items: list[dict]
    ) -> Optional[stripe.checkout.Session]:

        try:
            disconts_list: list[dict] = []
            disconts: QuerySet[Discount] = Discount.objects.filter(
                item=self.id
            )
            if disconts:
                coupon = stripe.Coupon.create(
                    percent_off=disconts.last().persent, 
                    duration="once"
                )
                disconts_list.append({
                    "coupon": coupon.id
                })

            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=settings.DOMAIN + '/success',
                cancel_url=settings.DOMAIN + '/cancel',
                discounts=disconts_list,
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


class OrderManager(models.Manager):
    """Manager for order."""

    def get_if_exist(
        self, 
        id: int
    ) -> Optional['Order']:

        try:
            return self.get(id=id)
        except ObjectDoesNotExist:
            return None


class Order(models.Model):
    """Order have one or many items."""

    datetime_created = models.DateTimeField(
        verbose_name="время создания",
        auto_created=True,
        auto_now=True
    )
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name="товар",
        related_name='order'
    )
    objects = OrderManager()

    class Meta:
        ordering = (
            '-datetime_created',
        )
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self) -> str:
        return f'Order by {self.datetime_created}'

    @cached_property
    def full_price(self) -> float:
        items: QuerySet[Item] = self.item.get_queryset()
        return float(
            items.aggregate(
                sum=Sum('price')
            ).get(
                'sum'
            )
        )


class Discount(models.Model):
    """Discount in the form of coupons."""

    MAX_PERSENT = 100

    # Can use Celery.
    datetime_ending = models.DateTimeField(
        verbose_name="время завершения скидки"
    )
    item = models.ManyToManyField(
        to=Item,
        verbose_name="товар",
        related_name='discont'
    )
    persent = models.PositiveSmallIntegerField(
        verbose_name="размер скидки",
        validators=[
            MaxValueValidator(MAX_PERSENT)
        ]
    )

    class Meta:
        ordering = (
            '-datetime_ending',
        )
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'

    def __str__(self) -> str:
        return self.item + " " + self.persent + "%"


class Tax(models.Model):
    """Tax for item."""

    item = models.ManyToManyField(
        to=Item,
        verbose_name="товар",
        related_name='tax'
    )
    display_name = models.CharField(
        verbose_name="название",
        max_length=200
    )
    inclusive = models.BooleanField(
        verbose_name="включает в стоимость",
        default=False
    )
    percentage = models.DecimalField(
        verbose_name="процент",
        max_digits=3,
        decimal_places=2,
        validators=[
            MaxValueValidator(100)
        ]
    )
    country = models.CharField(
        verbose_name="код страны",
        max_length=4,
        choices=(
            ('usd', 'USD'),
            ('eur', 'EUR'),
        )
    )
    description = models.TextField(
        verbose_name='описание'
    )

    class Meta:
        ordering = (
            '-percentage',
        )
        verbose_name = 'налог'
        verbose_name_plural = 'налоги'

    @cached_property
    def items_name(self) -> str:
        result: str = ""

        i: Item
        for i in self.item.get_queryset():
            result += i.name

        return result
