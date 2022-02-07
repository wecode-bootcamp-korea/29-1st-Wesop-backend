import uuid

from django.db import models
from products.models import Product
from users.models import User
from bases.models import Base

class OrderStatus(Base):
    order_status = models.CharField(max_length=100, blank=True)
    
    class meta:
        db_table = 'order_status'

class Order(Base):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at   = models.DateTimeField(auto_now=True)
    ordered_code = models.UUIDField(default=uuid.uuid4, editable=False)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderItem(Base):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status    = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity        = models.PositiveIntegerField(default=0)
    total_price     = models.PositiveIntegerField(default=0)
    tracking_number = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = 'order_items'
