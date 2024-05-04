from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    # foreign key to the CustomUser model making it a one-to-many relationship
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

# OrderItem model to store the order details making it a many-to-many relationship
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            raise ValidationError("Insufficient stock for product")
        self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)
