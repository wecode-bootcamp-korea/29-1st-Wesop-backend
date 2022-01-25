from django.db import models

class User(models.Model) :
    email = models.EmailField(max_length=300, unique=True)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=200)
    
    class Meta :
        db_table = 'users'

class User_detail(models.Model) :
    skintype = models.CharField(max_length=100, blank=True)
    recive_letter = models.CharField(max_length=2, default='F')
    
    class Meta :
        db_table = 'user_details'
        
class Address(models.Model) :
    nation_code = models.CharField(max_length=10, blank = True)
    city = models.CharField(max_length=100, blank = True)
    addr_detail = models.CharField(max_length=200, blank = True)
    phone = models.CharField(max_length=50, blank = True)
    post_number = models.CharField(max_length=50, blank = True)

    class Meta :
        db_table = 'addresses'