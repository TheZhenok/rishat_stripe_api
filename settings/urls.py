# Django
from django.contrib import admin
from django.urls import (
    path,
    include,
)
from django.conf import settings
from django.conf.urls.static import static

# DRF
from rest_framework.routers import DefaultRouter

# Apps
from orders.views import (
    ItemView,
    StripeItemView,
    OrderView,
    StripeOrderView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/<int:pk>/', ItemView.as_view(), name='item'),
    path('order/<int:pk>/', OrderView.as_view(), name='order'),
    path('api-auth/', include('rest_framework.urls'))
] + static(
    settings.STATIC_URL, 
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

# ---------------------------------------
# Api-Endpoints
# 
router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)
router.register('buy', StripeItemView)
router.register('buy/order', StripeOrderView)

urlpatterns += [
    path('',include(router.urls)),
]
