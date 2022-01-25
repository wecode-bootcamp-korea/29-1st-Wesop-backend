from django.db import models

class User(models.Model) :
    
    email           = models.EmailField(max_length=300, unique=True)
    password        = models.CharField(max_length=250)
    name            = models.CharField(max_length=200)
    phone           = models.CharField(max_length=45, blank=True)
    recive_letter   = models.BooleanField(default=False)
    skin_type       = models.ForeignKey()
    
    class Meta :
        db_table    = 'users'

class Address(models.Model) :
    
    user_id         = models.ForeignKey(User, on_delete= models.CASCADE)
    nation_code     = models.CharField(max_length=10, blank = True)
    city            = models.CharField(max_length=100, blank = True)
    addr_detail     = models.CharField(max_length=100, blank = True)
    post_number     = models.CharField(max_length=50, blank = True)

    class Meta :
        db_table    = 'addresses'