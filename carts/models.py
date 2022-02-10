from django.db import models
from bases.models import Base

from bases.models import Base
from users.models import User
from products.models import ProductOption

class Cart(Base):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'carts'