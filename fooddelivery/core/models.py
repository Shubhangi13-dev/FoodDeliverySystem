from django.db import models
from django.contrib.auth.models import User

# 1. FoodItem class sabse pehle aayegi
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

# 2. CartItem class sirf EK BAAR aayegi
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item.price * self.quantity

# 3. Order class
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending ⏳'),
        ('Preparing', 'Preparing 👨‍🍳'),
        ('Delivered', 'Delivered 🚚'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"