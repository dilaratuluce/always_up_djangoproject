from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),

    path('login/', views.LoginRequest.as_view(), name="login"),
    path('signin/', views.SigninRequest.as_view(), name="signin"),
    path('howitworks/', views.HowItWorks.as_view(), name="howitworks"),
    path('contact/', views.contact, name="contact"),
]