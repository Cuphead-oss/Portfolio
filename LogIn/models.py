from django.db import models

# Create your models here.
class User_Base(models.Model):
    #Blyattttttttttt
    name=models.CharField(max_length=100,primary_key=True)
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.name
