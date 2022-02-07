from django.db import models
from bases.models import Base

class MainCategory(Base):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'main_categories'

class SubCategory(Base):
    name          = models.CharField(max_length=200, blank=True)
    description   = models.TextField()
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Product(Base):
    name            = models.CharField(max_length=200)
    description     = models.TextField()
    ingredients_etc = models.TextField()
    sub_category    = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
      
class KeyIngredient(Base):
    name       = models.CharField(max_length=100)

    class Meta:
        db_table = 'key_ingredients'

class ProductOption(Base):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_options')
    size    = models.CharField(max_length=30)
    price   = models.DecimalField(null=True, default=0, decimal_places=3, max_digits=9)

    class Meta:
        db_table = 'products_options'

class ProductIngredient(Base):
    ingredient = models.ForeignKey(KeyIngredient, on_delete=models.CASCADE, related_name='ingredient_id')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_key_ingredient')

    class Meta:
        db_table = 'products_ingredients'

class Skintype(Base):
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'skintypes'

class ProductSkintype(Base):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_skin_type')
    skin    = models.ForeignKey(Skintype, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_skintypes'
