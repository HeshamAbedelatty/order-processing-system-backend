from django.urls import path
from store import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'products', views.ProductListView, basename='product')
router.register(r'place_order', views.PlaceOrderView, basename='place_order')
router.register(r'orders', views.OrderListView, basename='order')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]