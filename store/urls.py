from django.urls import path
from store import views
from .views import PaymentAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSets with it.
# The API URLs are now determined automatically by the router.
router = DefaultRouter()
router.register(r'products', views.ProductListView, basename='product')
router.register(r'place_order', views.PlaceOrderView, basename='place_order')
router.register(r'orders', views.OrderListView, basename='order')

urlpatterns = [
    # The API URLs are now determined automatically by the router.
    path('', include(router.urls)),
    
    # payment endpoint
    path('make_payment/', PaymentAPIView.as_view(), name='make_payment')
]