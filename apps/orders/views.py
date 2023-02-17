# Django
from django.shortcuts import render
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.conf import settings
from django.db.models import QuerySet

# DRF
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response

# Stripe
import stripe

# Local
from .mixins import (
    HttpResponseMixin,
    JsonResponseMixin,
)
from .models import (
    Item,
    Order,
    Discount
)


stripe.api_key = settings.STRIPE_PRIVATE_KEY

class ItemView(View, HttpResponseMixin):
    """View by Item."""

    template_name = 'orders/item.html'

    def get(
        self,
        request: WSGIRequest,
        pk: int,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        
        item: Item = Item.objects.get_if_exist(pk)
        discount_price: int = None
        if not item:
            return self.get_http_error(
                request=request,
                error_message=f"Object {pk} does not exist"
            )

        disconts: QuerySet[Discount] = Discount.objects.filter(
            item=item.id
        )
        if disconts:
            discount_price =\
                item.price * disconts.last().persent / 100 
            discount_price = item.price - discount_price

        return self.get_http_response(
            request=request,
            template_name=self.template_name,
            context={
                "ctx_obj": item,
                "ctx_discount_price": discount_price,
                "ctx_discount": disconts.last(),
                "ctx_stripe_pk": settings.STRIPE_PUBLIC_KEY
            }
        )


class OrderView(View, HttpResponseMixin):
    """View by Item."""

    template_name = 'orders/order.html'

    def get(
        self,
        request: WSGIRequest,
        pk: int,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        
        order: Order = Order.objects.get_if_exist(pk)
        if not order:
            return self.get_http_error(
                request=request,
                error_message=f"Object {pk} does not exist"
            )

        return self.get_http_response(
            request=request,
            template_name=self.template_name,
            context={
                "ctx_order": order,
                "ctx_objs": order.item.get_queryset(),
                "ctx_stripe_pk": settings.STRIPE_PUBLIC_KEY
            }
        )


class StripeItemView(ViewSet, JsonResponseMixin):
    """REST view for Stripe."""

    queryset: QuerySet[Item] = Item.objects.all()

    def retrieve(
        self, 
        request: DRF_Request, 
        pk: int = 0
    ) -> DRF_Response:
        """Handles GET-request with ID to show stripe id."""

        line_items: list[dict] = []
        item: Item = None
        try:
            item = self.queryset.get(id=pk)
        except Item.DoesNotExist:
            return self.get_json_response({
                'message': f'Object {pk} does not exist'
            })

        line_items = item.get_stripe_dict(line_items)
        checkout_session = item.get_stripe_session(line_items)
        if not checkout_session:
            return self.get_json_response({
                'message': 'Server error'
            }, 500)
        
        return self.get_json_response({
            "id": checkout_session.id
        })


class StripeOrderView(ViewSet, JsonResponseMixin):
    """REST view for Stripe."""

    queryset: QuerySet[Order] = Order.objects.all()

    def retrieve(
        self, 
        request: DRF_Request, 
        pk: int = 0
    ) -> DRF_Response:
        """Handles GET-request with ID to show stripe id."""

        line_items: list[dict] = []
        order: Order = None
        try:
            items = self.queryset.get(id=pk).item.get_queryset()
        except Item.DoesNotExist:
            return self.get_json_response({
                'message': f'Object {pk} does not exist'
            })
        
        item: Item
        for item in items:
            line_items = item.get_stripe_dict(line_items)

        checkout_session = item.get_stripe_session(line_items)
        if not checkout_session:
            return self.get_json_response({
                'message': 'Server error'
            }, 501)
        
        return self.get_json_response({
            "id": checkout_session.id
        })
