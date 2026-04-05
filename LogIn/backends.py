from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

user=get_user_model()

class EmailBack(ModelBackend):

   def authenticate(self, request, username = ..., password = ..., **kwargs):
       
       try:
           
           usr=user.objects.get(Q(username=username) | Q(email=username))
        
       except:
           
           return None
       
       if usr.check_password(password):
           return usr
       else:
           return None
