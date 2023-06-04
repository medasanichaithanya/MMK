from django.db import models

# Create your models here.

class Account(models.Model):
    auth_id = models.CharField(max_length=40)
    username  = models.CharField(max_length=30)

class Phone_number(models.Model):
    number = models.CharField(max_length=40)
    account_id = models.IntegerField()
