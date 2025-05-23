from django.db import models
from django.contrib.auth.models import AbstractUser
from deposits.models import DepositProducts, SavingProducts
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=11)
    age = models.IntegerField(default=20)
    email = models.CharField(max_length=20)
    gender = models.IntegerField(default=0) # 0: 남자, 1: 여자
    salary = models.IntegerField(default=0)
    wealth = models.IntegerField(default=0)
    deposit = models.ManyToManyField(DepositProducts, blank=True, related_name="joined")
    saving = models.ManyToManyField(SavingProducts, blank=True, related_name="joined2")