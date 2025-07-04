from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('send-otp/', views.send_otp, name='sendotp'),
    path('verify-otp/', views.verify_otp, name='verifyotp'),
    path('reset-password/', views.reset_password, name='resetpassword'),
    path('change-password/', views.change_password, name='changepassword'),
    path('logout/', views.logout, name='logout'),
]
