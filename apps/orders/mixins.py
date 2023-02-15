# Python
from typing import (
    Union,
    Optional
)

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.template import (
    loader,
    Template,
)

# DRF
from rest_framework.response import Response as DRF_Response


class HttpResponseMixin:
    """Mixin for send http response."""

    content_type: str = 'text/html'

    def get_http_response(
        self,
        request: WSGIRequest,
        template_name: str,
        context: dict = {}
    ) -> HttpResponse:

        template: Template =\
            loader.get_template(
                template_name
            )

        return HttpResponse(
            template.render(
                context=context,
                request=request
            ),
            content_type=self.content_type
        )

    def get_http_error(
        self,
        request: WSGIRequest,
        error_message: str
    ) -> HttpResponse:

        return self.get_http_response(
            request=request,
            template_name="error.html",
            context={
                "err": error_message
            }
        )


class JsonResponseMixin:
    """Json response mixin for DRF ViewSet."""

    def get_json_response(
        self,
        data: Union[dict, list],
        code: int = 200
    ) -> DRF_Response:
        """Get JSON response."""

        response: Optional[DRF_Response] = DRF_Response(
            data,
            status=code
        )

        return response
