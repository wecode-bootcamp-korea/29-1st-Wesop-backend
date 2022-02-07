from django.db import models
from bases.models import Base
from products.models import Skintype

class User(Base) :
    email           = models.EmailField(max_length=250, unique=True)
    password        = models.CharField(max_length=250)
    name            = models.CharField(max_length=200)
    phone           = models.CharField(max_length=45, blank=True)
    receive_letter  = models.BooleanField(default=False)
    skintype        = models.ForeignKey(Skintype, on_delete=models.CASCADE, null=True)

    class Meta :
        db_table    = 'users'


class Address(Base) :
    user            = models.ForeignKey(User, on_delete= models.CASCADE)
    nation_code     = models.CharField(max_length=10, blank = True)
    city            = models.CharField(max_length=100, blank = True)
    address_detail  = models.CharField(max_length=100, blank = True)
    post_number     = models.CharField(max_length=50, blank = True)

    class Meta :
        db_table    = 'addresses'

class ValidEmail(Base) :
    form_text       = models.CharField(max_length=100, blank=False)
    
    class Meta :
        db_table    = 'validemails'