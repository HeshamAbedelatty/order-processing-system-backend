from rest_framework import status
from rest_framework.response import Response

from store.permissions import IsOrderOwner
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer
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
    permission_classes = [IsAuthenticated,IsOrderOwner]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
    

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PaymentSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from allauth.account.utils import send_email_confirmation
from django.core.mail import send_mail

# Payment API View Simulation for processing payments for orders (POST request)
class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOrderOwner] 
    def post(self, request):
        orderid = request.data.get('order_id')
        
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_data = serializer.validated_data

            # Simulate Payment Processing (Mocked logic for testing)
            success = simulate_payment(payment_data)

            if success:
                # edit the order Paid from false to true
                order = Order.objects.get(id=orderid)
                # Check if the order exists
                if not order:
                    return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
                # Check if the order belongs to the customer
                if order.customer != request.user:
                    return Response({"message": "This order is not belogs to the customer"}, status=status.HTTP_403_FORBIDDEN)
                # Check if the order is already paid
                if order.paid:
                    return Response({"message": "Order is already paid"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Order fulfillment on successful payment
                # mark as paid
                order.paid = True
                
                order_items = OrderItem.objects.filter(order=order)
                
                # Create a list to store the item details
                item_details = []
                
                for item in order_items:
                    item_details.append({
                        "product": item.product.name,
                        "price": item.product.price,
                        "quantity": item.quantity,
                        "total price": item.product.price * item.quantity  # Calculate total price for the item
                    })
                # Return the order data
                order_data = {
                    "order_id": order.id,
                    "total_amount": order.total_amount,
                    "created_at": order.created_at,
                    "items": item_details  # Add the list of item details
                }
                # Send confirmation email
                subject = f"Hesham Store Order Confirmation - #{order.id}"
                to_email = order.customer.email
                text_content = "Your order confirmation email."  # Optional plain text content
                html_content = render_to_string('store/order_confirmation.html', {'order_data':order_data})
                # Assuming you have the actual email address in a variable named 'to_email'
                send_mail(subject, '', 'mohamed9999ah@gmail.com', [to_email], html_message=html_content)
                # Save the order
                order.save()
                response_data = {
                "message": "Payment successful",
                "order_data": order_data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Payment failed Invalid card number"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Luhn Algorithm for Credit Card Validation
def is_valid_card_number(card_number):
    # Remove any non-numeric characters
    card_number = ''.join(c for c in card_number if c.isdigit())

    # Check card length based on the first digit (optional)
    if not (len(card_number) in [15, 16]):
        return False

    # Luhn checksum calculation
    sum = 0
    is_second_digit = False
    for i, digit in enumerate(reversed(card_number)):
        digit = int(digit)
        if is_second_digit:
            digit = digit * 2
        sum += digit // 10 + digit % 10
        is_second_digit = not is_second_digit

    return (sum % 10) == 0

# Simulate Payment Processing (Replace with your external service call or script logic)
def simulate_payment(payment_data):
     # Check card number validity before simulating success/failure
    if not is_valid_card_number(payment_data['card_number']):
        return False

    # Simulate processing time 
    import time
    time.sleep(1)  # Simulate 1 second delay
    
    return True  
