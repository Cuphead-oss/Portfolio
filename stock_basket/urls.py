from django.urls import  path
from . import views
urlpatterns = [
    path('',views.Main,name="basket_main")
]
