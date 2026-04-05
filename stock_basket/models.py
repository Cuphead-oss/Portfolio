from django.db import models

# Create your models here.
class Stock(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    