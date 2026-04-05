from django.shortcuts import render,redirect
from .models import User_Base
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from .forms import Login_Form,Signup,Code
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponse
import secrets
import string
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import RedirectView
# Create your views here.

class Login(FormView):
    
   template_name="Login/Login.html"
   form_class=Login_Form
   success_url=reverse_lazy("Home")
   
   def form_valid(self, form):
      name_Email=form.cleaned_data['user_email']
      password=form.cleaned_data['password']
      user=authenticate(username=name_Email,password=password)
      
      if user:
       login(self.request,user)
       return super().form_valid(form)
      else:
         form.add_error(None, "Invalid credentials")
         return super().form_invalid(form)
   
   def form_invalid(self, form):
      return super().form_invalid(form)
   

class Sign_up(FormView):
   template_name="Login/sign_up.html"
   form_class=Signup
   success_url=reverse_lazy('Code')
   

   def form_valid(self, form):
      name=form.cleaned_data['name']
      email=form.cleaned_data['email']
      password=form.cleaned_data['password']
      
      usr=User.objects.filter( Q(username=name) | Q(email=email) ).exists()
   
      if usr is True:
         form.add_error('name','Name Or Email already in Use')
         return self.form_invalid(form)
      
      send_mail(self.request,name,email,password)

      return super().form_valid(form)
   
class Code_(FormView):
   template_name="LogIn/Code.html"
   form_class=Code
   success_url=reverse_lazy("Home")

   def get_context_data(self, **kwargs):

      context=super().get_context_data(**kwargs)
      key=self.request.session.get('signup_temp')
      
      total_time=key['Expires']
      current_time=time.time()

      if total_time<current_time:
         context['Resend_button']=True
      else:
         context['Resend_button']=False

      return context
   
   def form_valid(self, form):
      
      code=form.cleaned_data['code']
      key=self.request.session.get('signup_temp')

      if code==key['Code'] and key['Expires']>time.time():
         self.request.session.flush()

         u=User(username=key['Name'],email=key['Email'])
         u.save()
         u.set_password(key['Password'])

         login(self.request,u,backend='django.contrib.auth.backends.ModelBackend')
         return super().form_valid(form)
      
      elif code!=key['Code']:
         form.add_error('code','The Code entered is Worng')
         return self.form_invalid(form)
      
      else:
         form.add_error(None,'Code Expired')
         return self.form_invalid(form)

class ResendCode(RedirectView):
   pattern_name="Code"

   def get_redirect_url(self, *args, **kwargs):

      random_string = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
      key=self.request.session.get('signup_temp')

      self.request.session['signup_temp']={
        'Email': key['Email'],
        'Name': key['Name'],
        'Password': key['Password'],
        'Code': random_string,
        'By_Pass':True,
        'Expires': time.time() + 300  # expires in 5 minutes
   }

      subject, from_email, to = "You'r Protfolio Resended Code is:", 'subhyoyogg@gmail.com',f'{key['Email']}'
      random_string_=random_string
   
      html_content = render_to_string('LogIn/mail_template.html', {'Code':random_string_}) 
      text_content = strip_tags(html_content) 

      msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
      msg.attach_alternative(html_content, "text/html")
      msg.send()

      return super().get_redirect_url(*args, **kwargs)
            
#code sending
def send_mail(request,Name,Email,Pass):
   random_string = ''.join(
    secrets.choice(string.ascii_letters + string.digits)
    for _ in range(10)
)

   request.session['signup_temp']={
        'Email': Email,
        'Name': Name,
        'Password': Pass,
        'Code': random_string,
        'By_Pass':True,
        'Expires': time.time() + 300  # expires in 5 minutes
   }

   subject, from_email, to = "You'r Protfolio Code is:", 'subhyoyogg@gmail.com',f'{Email}'
   random_string_=random_string
   
   html_content = render_to_string('LogIn/mail_template.html', {'Code':random_string_}) 
   text_content = strip_tags(html_content) 

   msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
   msg.attach_alternative(html_content, "text/html")
   msg.send()
   