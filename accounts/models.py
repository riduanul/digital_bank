from django.db import models
from django.contrib.auth.models import User
from .constant import ACCOUNT_TYPE, GENDER_TYPE
# Create your models here.
# django amaderk built in user make korar facility day.

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete = models.CASCADE )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length= 10, choices=GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add = True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
   
    def __str__(self):
        return f'{self.account_no}'

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street = models.CharField(max_length=100) 
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100) 
    def __str__(self):
        return f'{self.user.email}'