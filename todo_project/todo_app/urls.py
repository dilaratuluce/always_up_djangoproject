from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('login/', views.LoginRequest.as_view(), name="login"),
    path('signin/', views.SigninRequest.as_view(), name="signin"),
    path('howitworks/', views.HowItWorks.as_view(), name="howitworks"),
    path('contact/', views.Contact.as_view(), name="contact"),
]
