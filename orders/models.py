from django.db import models
from products.models import Base, Product

class Cart(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'

class Order_Status(Base):
    order_status = models.CharField(max_length=100)
    
    class Meta:
        abstract = True

class Order(Base, Order_Status):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now=True)
    ordered_code =  models.CharField(max_length=200)

    class Meta:
        db_table = 'orders'

class Order_Item(Base, Order_Status):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    tracking_number = models.CharField(max_length=300)

    class Meta:
        db_table = 'order_items'
    
