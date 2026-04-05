from django.urls import path
from . import views
urlpatterns = [
    path("",views.Login.as_view(),name="Login"),
    path("/signup",views.Sign_up.as_view(),name="signup"),
    path("/code",views.Code_.as_view(),name="Code"),
    path("/resend_code",views.ResendCode.as_view(),name="Resend")
    
]
