from django.urls import include, path
from . import views
urlpatterns = [
    path('',views.HomePage.as_view(),name="Home"),
    path('search/',views.Search.as_view(),name="Search"),
    path('His_data/',views.Histroy_Price,name="History"),
    path('logout',views.Logout,name="LogOut"),
    
    #include:
    path('login',include('LogIn.urls')),
    path('mybasket/',include('stock_basket.urls'))
]