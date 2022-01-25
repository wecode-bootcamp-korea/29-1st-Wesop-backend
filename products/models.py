from pydoc import describe
from tkinter import CASCADE
from django.db import models
# from users import User

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Main_Category(Base):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'main_categories'

class Sub_Category(Base):
    name = models.CharField(max_length=200)
    description = models.TextField()
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_catogries'

class Product(Base):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients_etc = models.TextField()
    sub_category = models.ForeignKey(Sub_Category)

    class Meta:
        db_table = 'products'

class Product_Option(Base):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=30)
    price = models.PositiveIntegerField()

    class Meta:
        db_table = 'products_options'

class Key_Ingredients(Base):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'key_ingredients'

class Product_Ingredient(Base):
    ingredients = models.ForeignKey(Key_Ingredients, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_ingredients'

class Skintypes(Base):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'skintypes'

class Product_Skintype(Base):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    skin = models.ForeignKey(Skintypes, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_skintypes'

# class User(Base):
#     name = models.CharField(max_length=200)
#     skintype = models.ForeignKey(Skintypes, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=300)
#     password = models.CharField(max_length=250)
#     phone = models.CharField(max_length=45)
#     letter_received = models.BooleanField(default=False)

#     class Meta:
#         db_table = 'users'

# class Address(Base):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     detail = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     post_number = models.CharField(max_length=50)
#     nation_code = models.CharField(max_length=10)

#     class Meta:
#         db_table = 'addresses'    

class Cart(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'

# Order Status와 Order Item Status를 모두 처리
class Order_Status(Base):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'orders_statuses'

class Order(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey(Order_Status)
    ordered_at = models.DateTimeField(auto_now=True)
    ordered_code =  models.CharField(max_length=200)
    
    class Meta:
        db_table = 'orders'

class Order_Item(Base):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status = models.ForeignKey(Order_Status, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    tracking_number = models.CharField(max_length=300)

    class Meta:
        db_table = 'order_items'
    


