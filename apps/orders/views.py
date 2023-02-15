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
from .models import Item


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
        if not item:
            return self.get_http_error(
                request=request,
                error_message=f"Object {pk} does not exist"
            )

        return self.get_http_response(
            request=request,
            template_name=self.template_name,
            context={
                "ctx_obj": item,
                "ctx_stripe_pk": settings.STRIPE_PUBLIC_KEY
            }
        )


class StripeView(ViewSet, JsonResponseMixin):
    """REST view for Stripe."""

    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    queryset: QuerySet[Item] = \
        Item.objects.all()

    def retrieve(
        self, 
        request: DRF_Request, 
        pk: int = 0
    ) -> DRF_Response:
        """Handles GET-request with ID to show stripe id."""

        line_items: list[dict] = []
        item: Item = None
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return self.get_json_response({
                'message': f'Object {pk} does not exist'
            })
        line_items = item.get_stripe_dict(line_items)
        line_items = item.get_stripe_dict(line_items)
        checkout_session = item.get_stripe_session(line_items)
        if not checkout_session:
            return self.get_json_response({
                'message': 'Server error'
            }, 500)
        
        return self.get_json_response({
            "id": checkout_session.id
        })

        
