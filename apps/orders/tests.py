# Python
import unittest
import random

# Django
from django.test import TestCase
from django.core.exceptions import ValidationError

# Local
from .models import (
    Order,
    Item,
)


class ItemTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        for _ in range(200):
            price = random.randrange(50, 90, 5)
            Item.objects.create(
                name='Name',
                description='Temp description',
                price=price
            )

    def test_item_creation(self):
        item = Item.objects.create(
            name='Temp',
            description='Temp description',
            price=10
        )
        self.assertEqual(item.id, 201)

    def test_fail_creation(self):
        self.assertRaises(
            ValidationError, 
            Item.objects.create,
            name='Temp',
            description='description',
            price=-10
        )

    def test_get_does_not_exist(self):
        self.assertEqual(
            Item.objects.get_if_exist(1000),
            None
        )

    def test_get_stripe_dict(self):
        item: Item = Item.objects.create(
            name='Temp',
            description='Temp description',
            price=10
        )
        temp_list: list[dict] = []
        temp_list = item.get_stripe_dict(temp_list)
        temp_list = item.get_stripe_dict(temp_list)
        temp_list = item.get_stripe_dict(temp_list)
        self.assertEqual(
            len(temp_list),
            1
        )

    def test_get_stripe_dict_quantity(self):
        item: Item = Item.objects.create(
            name='Temp',
            description='Temp description',
            price=10
        )
        temp_list: list[dict] = []
        temp_list = item.get_stripe_dict(temp_list)
        temp_list = item.get_stripe_dict(temp_list)
        temp_list = item.get_stripe_dict(temp_list)
        self.assertEqual(
            temp_list[0].get('quantity'),
            3
        )
