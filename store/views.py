from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
# from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class ProductListView(viewsets.ModelViewSet):
    queryset = Product. objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class PlaceOrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_items = request.data.get("items", [])
        order = Order.objects.create(customer=request.user)
        total_amount = 0

        for item in order_items:
            product_name = item.get('productName')
            quantity = item.get('quantity')

            # Retrieve the product instance
            product = Product.objects.get(name=product_name)
            if not product:
                return Response({"error": "Product '{}' does not exist".format(product_name)}, status=status.HTTP_400_BAD_REQUEST)  
            if product.stock < quantity:
                return Response({"error": "Insufficient stock for product '{}'".format(product_name)}, status=status.HTTP_400_BAD_REQUEST)
            # Calculate total amount for the order
            total_amount += product.price * quantity

            # Create OrderItem for the current product
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        # Update the total amount for the order
        order.total_amount = total_amount
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class OrderListView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
